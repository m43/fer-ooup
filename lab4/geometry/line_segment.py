from typing import List

from geometry.abstract_graphical_object import AbstractGraphicalObject
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from point import Point
from rectangle import Rectangle
from renderer import Renderer


class LineSegment(AbstractGraphicalObject):
    def __init__(self, s: Point = Point(1, 1), e: Point = Point(11, 11)):
        super().__init__([s, e])

    def get_bounding_box(self) -> Rectangle:
        return GeometryUtil.bounding_box_from_points(self.hot_points)

    def selection_distance(self, mouse_point: Point) -> float:
        return GeometryUtil.distance_from_line_segment(self.get_start(), self.get_end(), mouse_point)

    def render(self, r: Renderer) -> None:
        r.draw_line(self.get_start(), self.get_end())

    def get_shape_name(self) -> str:
        return "Line"

    def clone(self) -> GraphicalObject:
        return LineSegment(self.get_start(), self.get_end())

    def get_start(self):
        return self.hot_points[0]

    def get_end(self):
        return self.hot_points[1]

    def get_shape_id(self) -> str:
        return "@LINE"

    def load(self, stack: List[GraphicalObject], data: str) -> None:
        parts = [int(s) for s in data.strip().split()]
        if len(parts) != 4:
            raise ValueError(
                "Need four numbers in string to load a line segment from string. Got this string '{}'.".format(data))

        s = Point(parts[0], parts[1])
        e = Point(parts[2], parts[3])
        stack.append(LineSegment(s, e))

    def save(self, rows: List[str]) -> None:
        s = self.get_start()
        e = self.get_end()
        rows.append("{} {} {} {} {}".format(self.get_shape_id(), s.x, s.y, e.x, e.y))
