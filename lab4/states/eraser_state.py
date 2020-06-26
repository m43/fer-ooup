# -*- coding: utf-8 -*-
from geometry.geometry_util import GeometryUtil
from model.document_model import DocumentModel
from painter_canvas import PainterCanvas
from point import Point
from states.idle_state import IdleState


class EraserState(IdleState):

    def __init__(self, dm: DocumentModel, canvas: PainterCanvas):
        self._dm = dm
        self._canvas = canvas
        self._points = set()
        self._objects = []
        self._last_point_added = None

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        self._points = {mouse_point}
        self._last_point_added = mouse_point
        self._objects = []

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        self._dm.remove_graphical_objects(self._objects)

    def mouse_dragged(self, mouse_point: Point) -> None:
        if GeometryUtil.distance_from_point(mouse_point, self._last_point_added) > 10:
            interpolated = Point((self._last_point_added.x + mouse_point.x) / 2,
                                 (self._last_point_added.y + mouse_point.y) / 2)
            self.mouse_dragged(interpolated)
            self.mouse_dragged(mouse_point)
            return

        if mouse_point not in self._points:
            self._points.add(mouse_point)
            self._canvas.draw_line(self._last_point_added, mouse_point)
            self._last_point_added = mouse_point
            self._objects.extend([go for go in self._dm.get_objects()
                                  if go not in self._objects and go.selection_distance(mouse_point) < 5])

    def on_leaving(self) -> None:
        self._canvas.redisplay()
