import attr
import math
from FreeCAD import Vector, Rotation

X_AXIS = Vector(1, 0, 0)

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

    # TODO: update these to support both offset and rotation.
    # Rotation of the next finger section.
    resting = attr.ib(default=[Rotation(X_AXIS, 10),
                               Rotation(X_AXIS, 20),
                               Rotation(X_AXIS, 20)])
    # Modifiers when actuating the key.
    # Can be a Rotation or a (Vector, Rotation) for an offset.
    actuate = attr.ib(default=[Rotation(X_AXIS, 13),
                               Rotation(X_AXIS, 20),
                               Rotation(X_AXIS, 20)])

    # [(Vector(0,10,-5), Rotation(X_AXIS, 0)),
    #   Rotation(X_AXIS, 20),
    #   Rotation(X_AXIS, 20)]

    @staticmethod
    def get_rots(angles):
        """Helper for easily generating rotations from a list of angles."""
        rots = []
        for a in angles:
            if a is not None:
                rots.append(Rotation(X_AXIS, -a))
            else:
                rots.append(None)
        return rots


@ attr.s
class Finger:
    """A single finger."""

    # TODO: Is the thumb a finger?

    # Offset of knuckle
    offset = attr.ib(default=Vector())

    # TODO: Maybe add a flex angle to calcuate neighbor column.
    # Lengths of the phalanges, ordered from closest from hand to furthest out.
    segments = attr.ib(default=[])

    # normal due to user reaching for key.
    # Angle between segments, starting with intial angle of first segment.
    rows = attr.ib(default=[
        Row().resting])

    @staticmethod
    def get_vecs(lengths):
        """Helper for getting a list of finger segment vectors."""
        return [Vector(0, d, 0) for d in lengths]

    def __str__(self):
        return '{}, {}'.format(self.segments, self.rows)

    def get_pos(self, modifiers):
        """Returns position vector for the resting tip of this finger."""
        v = Vector()
        for seg, mod in zip(self.segments, modifiers):
            if isinstance(mod, Rotation):
                v = v.add(mod.multVec(seg))
            elif isinstance(mod, Vector):
                v = v.add(mod).add(seg)
        return v.add(self.offset)

    def get_normal(self):
        """Returns the normal vector for a keypress from the current position."""
        # TODO: implement.
        # Normal should be calcuated for each key based on how the finger moves
        # to activate the key.


@ attr.s
class Hand:
    """A hand."""
    # Pinky first, counting towards inside.
    fingers = attr.ib(default=[Finger(), Finger(), Finger()])
