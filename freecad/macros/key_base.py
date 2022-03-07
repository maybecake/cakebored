from dataclasses import dataclass, field
import itertools
from typing import Dict, List
from FreeCAD import Vector
import Part

DIRECTIONS = {
    'left': Vector(-1, 0, 0),
    'right': Vector(1, 0, 0),
    'top': Vector(0, 0, -1),
    'bottom': Vector(0, 0, 1),
    'far': Vector(0, 1, 0),
    'close': Vector(0, -1, 0)
}

VECTOR_NAME_SEGMENTS = list(itertools.product(
    *[['far', 'close'], ['left', 'right'], ['top', 'bottom']]))


def make_box():
    vectors = {}

    for segments in VECTOR_NAME_SEGMENTS:
        key = "-".join(segments)
        vectors[key] = Vector(0, 0, 0)
        for pos in segments:
            vectors[key] += DIRECTIONS[pos]

    return vectors


@dataclass
class KeyBase:
    """Representation of the base of a key. Used to generate the webbing between
    adjacent keys to form the manifold of the keyboard."""

    vectors: Dict[str, Vector] = field(default_factory=make_box)

    def draw(self):
        print(self.vectors)

        lines = []
        names = list(itertools.product(
            *[['far'], ['left', 'right'], ['top', 'bottom']]))
        # Swap last two for correct vector drawing order.
        names[-1], names[-2] = names[-2], names[-1]
        for start, end in zip(names, names[1:] + names[:1]):
            start_pt = self.vectors['-'.join(start)]
            end_pt = self.vectors['-'.join(end)]
            line = Part.LineSegment(start_pt, end_pt)
            lines.append(line.toShape())
        wire = Part.Wire(lines)
        Part.show(wire)

        lines = []
        names = list(itertools.product(
            *[['close'], ['left', 'right'], ['top', 'bottom']]))
        # Swap last two for correct vector drawing order.
        names[-1], names[-2] = names[-2], names[-1]
        for start, end in zip(names, names[1:] + names[:1]):
            start_pt = self.vectors['-'.join(start)]
            end_pt = self.vectors['-'.join(end)]
            line = Part.LineSegment(start_pt, end_pt)
            lines.append(line.toShape())
        face = Part.Face(Part.Wire(lines))

        Part.show(face)

        # TODO: expand to other faces.
