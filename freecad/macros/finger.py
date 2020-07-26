import attr
import math
import utils
from FreeCAD import ActiveDocument, Vector, Rotation, Placement

X_AXIS = Vector(1, 0, 0)
Z_AXIS = Vector(0, 0, 1)
DOC = ActiveDocument

###############################################################################
# Coordinate system assumes hand looks like this:
#
#     | | | |          ^
#     | | | |  /       |
#     | | | | /        Y
#     O O O O        <Z|-X->  (Z is going away from you!)
#
###############################################################################


@attr.s
class Row:
    """Represents angles and mechanics required to hit a key in a certain row."""

    # Sidenote: Rotation(Vector(x,y,z),rot_radians) is a quaternion where (x,y,z) is
    # converted to a unit vector designating the axis of rotation.
    # for a fun trip: eater.net/quaternions

    # Modifiers for the resting position of finger segments.
    resting = attr.ib(default=[])

    # It turns out that there may be too many variables involved in calcuating a
    # true actuate positioning due the flexibily of finger in addition to the
    # contour of the finger tip.
    # Modifiers for the finger position when actuating a key. This is used to
    # calcuate the normal vector for the actual angling of the key.
    actuate = attr.ib(default=[])

    # Alternate method for specfying the angle of actuation for the keys.
    actuate_angle = attr.ib(default=None)

    @staticmethod
    def generate_mods(angles, offsets=None):
        """Helper for generating modifications from a list of angles."""
        if offsets is None:
            offsets = []
        mods = []
        utils.pad_list(angles, offsets)
        for a, o in zip(angles, offsets):
            if isinstance(a, Rotation):
                mods.append((o or Vector(), a))
            else:
                mods.append((o or Vector(), Rotation(X_AXIS, -a)))
        return mods

    def generate_actuate(self, diffs):
        """Generating an actuate position based.

        args:
            diffs: a list of (Vector, Rotation) diff pairs to apply to the resting list.
        """
        self.actuate = []
        utils.pad_list(self.resting, diffs)
        for base, diff in zip(self.resting, diffs):
            mod = base
            if diff is not None:
                (b_off, b_rot) = base
                (d_off, d_rot) = diff
                mod = (b_off + (d_off or Vector()), b_rot.multiply(d_rot))
            self.actuate.append(mod)


@ attr.s
class Finger:
    """A single finger's columns."""
    # Offset of knuckle
    offset = attr.ib(default=Vector())

    # Lengths of the phalanges, ordered from closest from hand to furthest out.
    segments = attr.ib(default=[])

    # list of Row objects, representing modifications to segments.
    rows = attr.ib(default=[])

    color = attr.ib(default=(0.2, 0.7, 0.5))

    @staticmethod
    def _apply_finger_offset(rots, offset):
        """Helper for applying an initial offset to each row position."""
        return Row.generate_mods(rots, [offset])

    def generate_segments(self, lengths):
        """Helper for generating a list of finger segment vectors."""
        self.segments = [Vector(0, d, 0) for d in lengths]
        return self

    def generate_rows(self, finger_offset, resting_rows):
        self.rows = []
        for rest_row in resting_rows:
            self.rows.append(
                Row(resting=Finger._apply_finger_offset(rest_row, finger_offset))
            )
        return self

    def __str__(self):
        return '{}, {}'.format(self.segments, self.rows)

    def get_pos(self, row_index, draw=False):
        """Returns position vector for the resting tip of this finger.

        args:
            row: List of (Vector, Rotation) to modify segment based on previous.
            draw: Wether to draw the segments.
            trans: Transparency of segment.

        returns:
            (Vector, rot) end position and rotation for normalizing key.
        """
        row = self.rows[row_index]
        if not row.actuate:
            row.generate_actuate([(None, Rotation(X_AXIS, -2))])

        rest_v = self._get_pos(row.resting, draw)
        act_v = self._get_pos(row.actuate, draw, trans=80)
        rot = Rotation(Z_AXIS, rest_v - act_v)
        return rest_v, rot

    def _get_pos(self, row, draw, trans=0):
        # Base vector for each section.
        base_v = Vector()
        rot_cumulative = Rotation()
        for seg, (off, rot) in zip(self.segments, row):
            base_v += off
            rot_cumulative = rot_cumulative.multiply(rot)
            if draw:
                self._draw_segment(base_v, seg, rot_cumulative, trans)
            base_v += rot_cumulative.multVec(seg)
        return base_v

    def _draw_segment(self, base_v, seg, rot, trans=0):
        """Draws a vector."""
        c = DOC.addObject("Part::Cone", 'cone')
        c.Height = seg.Length
        c.Radius1 = 3
        c.Radius2 = 1
        c.ViewObject.ShapeColor = self.color
        c.ViewObject.Transparency = trans
        c.Placement.Base = base_v
        c.Placement.Rotation = rot.multiply(Rotation(X_AXIS, 270))
        DOC.recompute()
