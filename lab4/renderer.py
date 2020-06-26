from abc import ABC, abstractmethod
from typing import List

from point import Point


class Renderer(ABC):
    @abstractmethod
    def draw_line(self, s: Point, e: Point):
        """
        Draw line from start to end
        :param s: start point
        :param e: end point
        """
        pass

    @abstractmethod
    def fill_polygon(self, points: List[Point]):
        """
        Draw filled polygon from given points
        :param points: The points of polygon
        """
        pass