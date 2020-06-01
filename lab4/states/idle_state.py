from geometry.graphical_object import GraphicalObject
from point import Point
from renderer import Renderer
from states.state import State


class IdleState(State):
    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    def mouse_dragged(self, mouse_point: Point) -> None:
        pass

    def key_pressed(self, key_event):
        pass

    def after_draw(self, r: Renderer, go: GraphicalObject):
        pass

    def after_draw_done(self, r: Renderer):
        pass

    def on_leaving(self):
        pass
