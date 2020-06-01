from __future__ import annotations

import math
from typing import List

from geometry.graphical_object import GraphicalObject
from point import Point
from rectangle import Rectangle
from renderer import Renderer


class GeometryUtil:

    @staticmethod
    def dot_of_points(v1: Point, v2: Point):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def distance_from_point(p1: Point, p2: Point) -> float:
        return GeometryUtil.vector_norm(Point(p1.x - p2.x, p1.y - p2.y))

    @staticmethod
    def vector_norm(v: Point):
        return math.sqrt((v.x) ** 2 + (v.y) ** 2)

    @staticmethod
    def distance_from_line_segment(s: Point, e: Point, p: Point) -> float:
        vector_se = e.difference(s)
        vector_se_norm = GeometryUtil.vector_norm(vector_se)
        vector_sp = p.difference(s)
        vector_sp_norm = GeometryUtil.vector_norm(vector_sp)

        dot = GeometryUtil.dot_of_points(vector_se, vector_sp)
        dot = dot / (vector_se_norm ** 2)
        if dot > 1:
            return GeometryUtil.distance_from_point(e, p)
        elif dot < 0:
            return GeometryUtil.distance_from_point(s, p)

        projection = Point(s.x + dot * vector_se.x, s.y + dot * vector_se.y)
        return GeometryUtil.distance_from_point(projection, p)

    @staticmethod
    def bounding_box_from_points(points: List[Point]):
        xmin, xmax, ymin, ymax = points[0].x, points[0].x, points[0].y, points[0].y
        for p in points:
            xmin = min(xmin, p.x)
            xmax = max(xmax, p.x)
            ymin = min(ymin, p.y)
            ymax = max(ymax, p.y)

        return Rectangle(xmin, ymin, xmax - xmin, ymax - ymin)

    @staticmethod
    def render_hot_points(r: Renderer, go: GraphicalObject):
        for hp_idx in range(go.get_number_of_hot_points()):
            GeometryUtil.render_hot_point(r, go.get_hot_point(hp_idx))

    @staticmethod
    def render_hot_point(r: Renderer, hp: Point, dx=6, dy=6):
        GeometryUtil.render_rectangle(r, Rectangle(hp.x - dx, hp.y - dy, 2 * dx, 2 * dy))

    @staticmethod
    def render_rectangle(renderer: Renderer, rect: Rectangle):
        for s in [Point(rect.x, rect.y), Point(rect.x + rect.width, rect.y + rect.height)]:
            for e in [Point(rect.x + rect.width, rect.y), Point(rect.x, rect.y + rect.height)]:
                renderer.draw_line(s, e)
