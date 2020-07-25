import attr
import math


@attr.s
class Finger(object):

    # Proximal phalanges length. Closest section to hand.
    prox_mm = attr.ib(default=44)
    mid_mm = attr.ib(default=23)   # Middle phalanges length. Middle part.
    dist_mm = attr.ib(default=18)  # Distal phalanges length. Finger tip.

    p_deg = attr.ib(default=math.pi/2)     # Angle of proximal.
    pm_deg = attr.ib(default=0)    # Angle between proximal and middle.
    md_deg = attr.ib(default=0)    # Angle between middle and distal.

    def get_total(self):
        return self.prox_mm + self.mid_mm + self.dist_mm

    def get_pos(self):
        x = math.cos(self.p_deg)*self.prox_mm + math.cos(self.pm_deg+self.p_deg) * \
            self.mid_mm + math.cos(self.md_deg +
                                   self.pm_deg+self.p_deg)*self.dist_mm
        y = math.sin(self.p_deg)*self.prox_mm + math.sin(self.pm_deg+self.p_deg) * \
            self.mid_mm + math.sin(self.md_deg +
                                   self.pm_deg+self.p_deg)*self.dist_mm
        return (x, y)
