# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from geometry.graphical_object import GraphicalObject, GraphicalObjectListener
from point import Point


class DocumentModelListener(ABC):
    @abstractmethod
    def document_change(self, dm: DocumentModel):
        pass


class DocumentModel(ABC):
    SELECTION_PROXIMITY = 12

    def __init__(self):
        self.__objects: List[GraphicalObject] = []
        self.__selected_objects: List[GraphicalObject] = []

        self._dm_listeners: List[DocumentModelListener] = []
        self.__go_listener = type(
            "DocumentModelAsGraphicalObjectListener", (GraphicalObjectListener, object),
            {"graphical_object_changed": lambda _, go,: self.notify_document_model_listeners(),
             "graphical_object_selection_changed": lambda _, go: self._selection_changed(go)})()

    def _selection_changed(self, go: GraphicalObject):
        if go.is_selected() and go not in self.__selected_objects:
            self.__selected_objects.append(go)
        elif not go.is_selected() and go in self.__selected_objects:
            self.__selected_objects.remove(go)

        self.notify_document_model_listeners()

    def clear(self) -> None:
        for go in self.__objects:
            go.remove_graphical_object_listener(self.__go_listener)

        self.__objects.clear()
        self.__selected_objects.clear()
        self.notify_document_model_listeners()

    def attach_document_model_listener(self, listener: DocumentModelListener) -> None:
        self._dm_listeners.append(listener)

    def detach_document_model_listener(self, listener: DocumentModelListener) -> None:
        self._dm_listeners.remove(listener)

    def notify_document_model_listeners(self) -> None:
        for listener in self._dm_listeners:
            listener.document_change(self)

    def add_graphical_object(self, go: GraphicalObject) -> None:
        self.insert_graphical_object(go, len(self.__objects) - 1)

    def insert_graphical_object(self, go: GraphicalObject, z_position: int):
        self.__objects.insert(z_position, go)
        go.add_graphical_object_listener(self.__go_listener)
        self.notify_document_model_listeners()

    def remove_graphical_objects(self, goes: List[GraphicalObject]):
        for go in goes:
            go.remove_graphical_object_listener(self.__go_listener)
            self.__objects.remove(go)
            if go.is_selected():
                self.__selected_objects.remove(go)
        self.notify_document_model_listeners()

    def get_objects(self) -> Tuple[GraphicalObject]:
        # TODO do i need to forbid the change of go objects inside this tuple?
        return tuple(self.__objects)

    def get_selected_objects(self) -> Tuple[GraphicalObject]:
        return tuple(self.__selected_objects)

    def increase_z(self, go: GraphicalObject) -> None:
        idx = self.__objects.index(go)
        if idx != len(self.__objects) - 1:
            self.__objects[idx], self.__objects[idx + 1] = self.__objects[idx + 1], self.__objects[idx]
        self.notify_document_model_listeners()

    def decrease_z(self, go: GraphicalObject) -> None:
        idx = self.__objects.index(go)
        if idx != 0:
            self.__objects[idx - 1], self.__objects[idx] = self.__objects[idx], self.__objects[idx - 1]
        self.notify_document_model_listeners()

    def find_selected_graphical_object(self, mouse_point: Point) -> GraphicalObject:
        result = None
        result_distance = None
        for go in self.__objects:
            distance = go.selection_distance(mouse_point)
            if distance <= self.SELECTION_PROXIMITY:
                if result_distance is None or result_distance > distance:
                    result = go
                    result_distance = distance
        return result

    def find_selected_hot_point(self, go: GraphicalObject, mouse_point: Point) -> int:
        result_idx = -1
        result_distance = None
        for idx in range(go.get_number_of_hot_points()):
            distance = go.get_hot_point_distance(idx, mouse_point)
            if distance <= self.SELECTION_PROXIMITY:
                if result_distance is None or result_distance > distance:
                    result_idx = idx
                    result_distance = distance
        return result_idx
