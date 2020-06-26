from abc import ABC, abstractmethod

from geometry.graphical_object import GraphicalObject
from point import Point
from renderer import Renderer


class State(ABC):
    @abstractmethod
    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    @abstractmethod
    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    @abstractmethod
    def mouse_dragged(self, mouse_point: Point) -> None:
        pass

    @abstractmethod
    def key_pressed(self, key_event):
        pass

    @abstractmethod
    def after_draw(self, r: Renderer, go: GraphicalObject) -> None:
        pass

    @abstractmethod
    def after_draw_done(self, r: Renderer) -> None:
        pass

    @abstractmethod
    def on_leaving(self) -> None:
        pass
