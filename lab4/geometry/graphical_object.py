# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, List

from point import Point
from rectangle import Rectangle
from renderer import Renderer

T = TypeVar('T')


class GraphicalObject(ABC):
    """
    Class modeling an abstract graphical object that supports hot points, selection of the object and hot points,
    saving and loading the object
    """

    # TODO Model vektorskog crteža treba sadržavati listu referenci na grafičke objekte koje trebaju koristiti
    #  različiti drugi objekti. Predloženi model prikazan je u nastavku i nudi jedinstveno sučelje prema svim svojim
    #  korisnicima (što može i ne mora biti dobro -- razmislite je li ovakav unificirani pristup u skladu s
    #  postojećim načelima oblikovanja?).

    @abstractmethod
    def is_selected(self) -> bool:
        pass

    @abstractmethod
    def set_selected(self, selected: bool) -> None:
        pass

    @abstractmethod
    def get_number_of_hot_points(self) -> int:
        pass

    @abstractmethod
    def get_hot_point(self, index: int) -> Point:
        pass

    @abstractmethod
    def set_hot_point(self, index: int, point: Point) -> None:
        pass

    @abstractmethod
    def is_hot_point_selected(self, index: int) -> bool:
        pass

    @abstractmethod
    def set_hot_point_selected(self, index: int, selected: bool) -> None:
        pass

    @abstractmethod
    def get_hot_point_distance(self, index: int, mouse_point: Point) -> float:
        pass

    # Geometrijska operacija nad oblikom
    @abstractmethod
    def translate(self, delta: Point) -> None:
        pass

    @abstractmethod
    def get_bounding_box(self, ) -> Rectangle:
        pass

    @abstractmethod
    def selection_distance(self, mouse_point: Point) -> float:
        pass

    # Podrška za crtanje (self, dio mosta)
    @abstractmethod
    def render(self, r: Renderer) -> None:
        pass

    # Observer za dojavu promjena modelu
    @abstractmethod
    def add_graphical_object_listener(self, l: GraphicalObjectListener) -> None:
        pass

    @abstractmethod
    def remove_graphical_object_listener(self, l: GraphicalObjectListener) -> None:
        pass

    # Podrška za prototip (self, alatna traka, stvaranje objekata u crtežu, ...)
    @abstractmethod
    def get_shape_name(self) -> str:
        pass

    @abstractmethod
    def clone(self) -> GraphicalObject:
        pass

    # Podrška za snimanje i učitavanje
    @abstractmethod
    def get_shape_id(self, ) -> str:
        pass

    @abstractmethod
    def load(self, stack: List[GraphicalObject], data: str) -> None:
        pass

    @abstractmethod
    def save(self, rows: List[str]) -> None:
        pass


class GraphicalObjectListener(ABC):
    """
    Class modeling GraphicalObject listeners.
    """

    @abstractmethod
    def graphical_object_changed(self, go: GraphicalObject) -> None:
        """
        Gets called if any change occurs to the object
        :param go: the graphical object that changed
        """
        pass

    @abstractmethod
    def graphical_object_selection_changed(self, go: GraphicalObject) -> None:
        """
        Gets called if the selection status of the graphical object got changed
        :param go: the graphical object that got changed
        """
        pass