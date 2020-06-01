from geometry.composite_shape import CompositeShape
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from model.document_model import DocumentModel
from point import Point
from renderer import Renderer
from states.state import State


class SelectshapeState(State):

    def __init__(self, dm: DocumentModel):
        self._dm = dm
        self.__hp_idx = -1
        self.__go = None

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        if not ctrl_down:
            for go in self._dm.get_objects():
                go.set_selected(False)

        self._select_object(mouse_point)

    def mouse_dragged(self, mouse_point: Point) -> None:
        if self.__hp_idx != -1:
            self.__go.set_hot_point(self.__hp_idx, mouse_point)

    def _select_object(self, point: Point):
        selected_object = self._dm.find_selected_graphical_object(point)
        if selected_object:
            selected_object.set_selected(True)

        selected_objects = self._dm.get_selected_objects()
        if len(selected_objects) == 1:
            self.__go = selected_objects[0]
            self.__hp_idx = self._dm.find_selected_hot_point(selected_objects[0], point)
        else:
            self.__go = None
            self.__hp_idx = -1

    def after_draw(self, r: Renderer, go: GraphicalObject):
        if go.is_selected():
            GeometryUtil.render_rectangle(r, go.get_bounding_box())

    def after_draw_done(self, r: Renderer):
        selected_objects = self._dm.get_selected_objects()
        if len(selected_objects) == 1:
            GeometryUtil.render_hot_points(r, selected_objects[0])

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    def key_pressed(self, key_event):
        selected_objects = self._dm.get_selected_objects()
        for go in selected_objects:
            if key_event.keysym == "Left":
                go.translate(Point(-1, 0))
            elif key_event.keysym == "Right":
                go.translate(Point(1, 0))
            elif key_event.keysym == "Up":
                go.translate(Point(0, -1))
            elif key_event.keysym == "Down":
                go.translate(Point(0, 1))

        if len(selected_objects) == 1:
            go = selected_objects[0]
            if key_event.keysym == "plus":
                self._dm.increase_z(go)
            elif key_event.keysym == "minus":
                self._dm.decrease_z(go)
            elif key_event.keysym == "u":  # ungroup
                if isinstance(go, CompositeShape):
                    idx = self._dm.get_objects().index(go)
                    for child in go.get_children():
                        self._dm.insert_graphical_object(child, idx)
                        child.set_selected(True)
                        idx += 1
        elif len(selected_objects) > 1:
            if key_event.keysym == "g":  # group
                selected_objects = list(selected_objects)
                for go in selected_objects:
                    go.set_selected(False)
                self._dm.remove_graphical_objects(selected_objects)
                combo = CompositeShape(selected_objects)
                self._dm.add_graphical_object(combo)
                combo.set_selected(True)

    def on_leaving(self):
        for go in self._dm.get_selected_objects():
            go.set_selected(False)
