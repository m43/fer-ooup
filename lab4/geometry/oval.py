import math
from typing import List

from geometry.abstract_graphical_object import AbstractGraphicalObject
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from point import Point
from rectangle import Rectangle
from renderer import Renderer


class Oval(AbstractGraphicalObject):

    def __init__(self, bottom: Point = Point(10, 0), right: Point = Point(0, 10)):
        super().__init__([bottom, right])

    def get_bottom_point(self):
        return self.hot_points[0]

    def get_right_point(self):
        return self.hot_points[1]

    def get_center_point(self):
        return Point(self.get_bottom_point().x, self.get_right_point().y)

    def get_bounding_box(self) -> Rectangle:
        c = self.get_center_point()
        right_to_center = c.difference(self.get_right_point())
        bottom_to_center = c.difference(self.get_bottom_point())
        top_left_corner = c.translate(right_to_center).translate(bottom_to_center)
        return GeometryUtil.bounding_box_from_points([self.get_bottom_point(), self.get_right_point(), top_left_corner])

    def selection_distance(self, mouse_point: Point) -> float:
        c = self.get_center_point()
        a = GeometryUtil.distance_from_point(c, self.get_right_point())
        b = GeometryUtil.distance_from_point(c, self.get_bottom_point())
        if (mouse_point.x - c.x) ** 2 / a ** 2 + (mouse_point.y - c.y) ** 2 / b ** 2 <= 1:
            return 0

        min_distance = -1
        n_points = 72
        for x in range(n_points):
            p_x = Point(c.x + a * math.cos(x * 2 * math.pi / n_points), c.y + b * math.sin(x * 2 * math.pi / n_points))
            distance = GeometryUtil.distance_from_point(p_x, mouse_point)
            if min_distance == -1 or min_distance > distance:
                min_distance = distance

        return min_distance

    def render(self, r: Renderer) -> None:
        c = self.get_center_point()
        a = GeometryUtil.distance_from_point(c, self.get_right_point())
        b = GeometryUtil.distance_from_point(c, self.get_bottom_point())
        points = []
        n_points = 72
        for x in range(n_points + 1):
            points.append(
                Point(c.x + a * math.cos(x * 2 * math.pi / n_points), c.y + b * math.sin(x * 2 * math.pi / n_points)))
        r.fill_polygon(points)

    def get_shape_name(self) -> str:
        return "Oval"

    def clone(self) -> GraphicalObject:
        return Oval(self.get_bottom_point(), self.get_right_point())

    def get_shape_id(self) -> str:
        return "@OVAL"

    def load(self, stack: List[GraphicalObject], data: str) -> None:
        parts = [int(s) for s in data.strip().split()]
        if len(parts) != 4:
            raise ValueError(
                "Need four numbers in string to load an oval from string. Got this string '{}'.".format(data))

        r = Point(parts[0], parts[1])
        b = Point(parts[2], parts[3])
        stack.append(Oval(b, r))

    def save(self, rows: List[str]) -> None:
        b = self.get_bottom_point()
        r = self.get_right_point()
        rows.append("{} {} {} {} {}".format(self.get_shape_id(), b.x, b.y, r.x, r.y))
