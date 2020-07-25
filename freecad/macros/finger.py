import attr
import math
from FreeCAD import Vector


@attr.s
class Finger:
    """A single finger."""

    # TODO: Maybe add a flex angle to calcuate neighbor column.
    # Lengths of the phalanges, ordered from closest from hand to furthest out.
    segments_mm = attr.ib(default=[44, 23, 18])

    # TODO: maybe also allow for non-straight fingers?
    # normal due to user reaching for key.
    # Angle between segments, starting with intial angle of first segment.
    rows = attr.ib(default=[
        [90, 0, 0],
        [90, 15, 15],
        [90, 45, 45]])

    def __str__(self):
        return '{}, {}'.format(self.segments_mm, self.angles_deg)

    def get_pos(self, angles, offset=Vector()):
        """Returns position coordinates for the tip of this finger"""
        ang_sum = 0
        v = Vector()
        for seg, ang in zip(self.segments_mm, angles):
            ang_sum += math.radians(ang)
            v.y += math.cos(ang_sum)*seg
            v.z += math.sin(ang_sum)*seg
        return v.add(offset)

    def get_normal(self):
        """Returns the normal vector for a keypress from the current position."""
        # TODO: implement.
        # Normal should be calcuated for each key based on how the finger moves
        # to activate the key.


@ attr.s
class Hand:
    """A hand."""
    fingers = attr.ib(default=[Finger(), Finger(), Finger()])

    # Knuckle offsets from 0.
    offsets = attr.ib(default=[Vector(), Vector(25, 10, 0), Vector(50, 0, 0)])
