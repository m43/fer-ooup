from typing import List

from geometry.abstract_graphical_object import AbstractGraphicalObject
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from point import Point
from rectangle import Rectangle
from renderer import Renderer


class CompositeShape(AbstractGraphicalObject):

    def __init__(self, children: List[GraphicalObject]):
        super().__init__([])
        self._children: List[GraphicalObject] = children

    def get_children(self):
        return tuple(self._children)

    def get_bounding_box(self) -> Rectangle:
        points = []
        for child in self._children:
            bbox = child.get_bounding_box()
            points.append(Point(bbox.x, bbox.y))
            points.append(Point(bbox.x + bbox.width, bbox.y + bbox.height))

        return GeometryUtil.bounding_box_from_points(points)

    def translate(self, delta: Point) -> None:
        for child in self._children:
            child.translate(delta)
        self.notify_listeners()

    def selection_distance(self, mouse_point: Point) -> float:
        min_distance = -1
        for child in self._children:
            distance = child.selection_distance(mouse_point)
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        # TODO how is this actually expected to behave?
        return min_distance

    def render(self, r: Renderer) -> None:
        for child in self._children:
            child.render(r)

    def get_shape_name(self) -> str:
        return "Composite"

    def clone(self) -> GraphicalObject:
        raise Exception("Composite cannot be cloned")

    def get_shape_id(self) -> str:
        return "@COMP"

    def load(self, stack: List[GraphicalObject], data: str) -> None:
        parts = [int(s) for s in data.strip().split()]
        if len(parts) != 1:
            raise ValueError(
                "Need exactly one number in string to load a composite. Got this string '{}'.".format(data))
        n_children = parts[0]

        children = stack[-n_children:]
        stack[-n_children:] = []
        if len(children) != n_children:
            raise ValueError("Not enough objects on stack to load the composite")

        stack.append(CompositeShape(children))

    def save(self, rows: List[str]) -> None:
        for child in self._children:
            child.save(rows)

        rows.append("{} {}".format(self.get_shape_id(), len(self._children)))
