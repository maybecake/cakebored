"""Finger position objects."""

from dataclasses import dataclass, field
from email.policy import default
from typing import List
import utils
from FreeCAD import ActiveDocument, Vector, Rotation, Placement


# TODO: refactor this out so that drawing is optional
DOC = ActiveDocument

X_AXIS = Vector(1, 0, 0)
Z_AXIS = Vector(0, 0, 1)


@dataclass
class Row:
    """Represents offsets and angles required to hit a key in a certain row."""

    # Sidenote: Rotation(Vector(x,y,z),rot_radians) is a quaternion where
    # (x,y,z) is converted to a unit vector designating the axis of rotation.
    # for a fun trip: eater.net/quaternions

    # Modifiers for the resting position of finger segments.
    resting: List = field(default_factory=lambda: [])

    # Rotation of actuation for the key.
    actuate_angle: Rotation = None

    # TODO: investigate inverse kinematics to calculate and optimize possible
    # position space.

    # Modifiers for the finger position when actuating a key. This is used to
    # calculate the normal vector for the actual angling of the key. It turns
    # out that there may be too many variables involved in calculating a true
    # actuate positioning due the flexibly of finger in addition to the contour
    # of the finger tip.
    actuate: List = field(default_factory=lambda: [])

    def generate_resting(self, offsets, angles):
        """Helper for generating modifications from a list of angles."""
        self.resting = []
        utils.pad_list(angles, offsets)
        for angle, offset in zip(angles, offsets):
            if isinstance(angle, Rotation):
                self.resting.append((offset or Vector(), angle))
            else:
                # Assume angle is a number.
                self.resting.append(
                    (offset or Vector(), Rotation(X_AXIS, -angle)))
        return self

    def generate_actuate(self, diffs):
        """Generating an actuate position based.

        args:
            diffs: a list of (Vector, Rotation) diff pairs to apply to the resting list.
        """
        self.actuate = []
        utils.pad_list(self.resting, diffs)
        print(self.resting, diffs)
        for base, diff in zip(self.resting, diffs):
            mod = base
            if diff is not None:
                (b_off, b_rot) = base
                (d_off, d_rot) = diff
                mod = (b_off + (d_off or Vector()), b_rot.multiply(d_rot))
            self.actuate.append(mod)
        return self


@dataclass
class Finger:
    """A single finger's columns."""
    # Hint: A knuckle offset can be set as an offset in the first modifier in
    # the Row position modifiers.

    # Lengths of the phalanges, ordered from closest from hand to furthest out.
    segments: List = field(default_factory=lambda: [])

    # List of Row objects, representing modifications to segments for each 'row'
    # of keys.
    rows: List = field(default_factory=lambda: [])

    # Key object associated with this finger.
    keys: List = field(default_factory=lambda: [])

    # (float R, float G, float B) display color for this finger.
    color: List = (0.2, 0.7, 0.5)

    def __str__(self):
        return '{}, {}'.format(self.segments, self.rows)

    def generate_segments(self, lengths):
        """Helper for generating a list of finger segment vectors."""
        self.segments = [Vector(0, d, 0) for d in lengths]
        return self

    def add_rows(self, initial_offset, rows):
        """Appends a list of rows."""
        print(self.rows)
        for (rest_row, angle) in rows:
            row = Row(actuate_angle=Rotation(X_AXIS, angle))
            row.generate_resting([initial_offset], rest_row)
            self.rows.append(row)
        return self

    def get_pos(self, row_index, draw=False):
        """Returns position vector for the resting tip of this finger.

        args:
            row: List of(Vector, Rotation) to modify segment based on previous.
            draw: Wether to draw the segments.
            trans: Transparency of segment.

        returns:
            (Vector, rot) end position and rotation for normalizing key.
        """
        row = self.rows[row_index]
        rest_v = self._get_pos(row.resting, draw)
        rot = row.actuate_angle

        if not rot:
            # If actuation angle is not defined, calculate with actuate
            # position.
            if not row.actuate:
                row.generate_actuate([(None, Rotation(X_AXIS, -2))])
            act_v = self._get_pos(row.actuate, draw, trans=80)
            rot = Rotation(Z_AXIS, rest_v - act_v)

        return rest_v, rot

    def get_base_pos(self, unused_row_index):
        """Returns the position of the verticies for the base of the key.

        args:
            row_index:
        returns:
            Vector position for the key base.
        """
        # rest_v, rot = self.get_pos(row_index)
        return

    def _get_pos(self, mods, draw, trans=0):
        # Base vector for each section.
        base_v = Vector()
        rot_cumulative = Rotation()
        for seg, (off, rot) in zip(self.segments, mods):
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

    # Unused?
    # @ staticmethod
    # def _apply_finger_offset(rots, offset):
    #     """Helper for applying an initial offset to each row position."""
    #     return Row.generate_mods(rots, [offset])
