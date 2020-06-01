from __future__ import annotations


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def translate(self, dp: Point) -> Point:
        """
        :param dp: Point to translate by
        :return: this+dp aka new point that is the result of translating the current point by dp
        """
        return Point(self.x + dp.x, self.y + dp.y)

    def difference(self, p: Point) -> Point:
        """
        :param p: point to subtract by
        :return: this-p aka new point that is the result of taking the difference between this point and the given point
        """
        return Point(self.x - p.x, self.y - p.y)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "({},{})".format(self.x, self.y)
