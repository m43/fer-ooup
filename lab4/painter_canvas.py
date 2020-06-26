# -*- coding: utf-8 -*-
from tkinter import Canvas, BOTH, EventType, BOTTOM
from typing import List

from flat_colors import FlatUiColors
from model.document_model import DocumentModel, DocumentModelListener
from point import Point
from renderer import Renderer
from states.idle_state import IdleState
from states.state import State


class PainterCanvas(Canvas, Renderer):
    def __init__(self, document_model: DocumentModel, bg_color="#000", outline_color=FlatUiColors.CLOUDS,
                 fill_color=FlatUiColors.EMERALD, **kw):
        super().__init__(bg=bg_color, **kw)
        self._current_state: State = IdleState()  # TODO where should current state be? gui or canvas?
        self._dm = document_model
        self._dm_listener = type("DMListener", (DocumentModelListener, object),
                                 {"document_change": lambda _, __: self.redisplay()})()
        self._dm.attach_document_model_listener(self._dm_listener)
        self._bg_color = bg_color
        self._outline_color = outline_color
        self._fill_color = fill_color
        self.pack(side=BOTTOM, fill=BOTH, expand=1)

        self.bind_all("<Key>", self.on_key_pressed)
        self.bind("<ButtonPress-1>", self.on_left_mouse_action)
        self.bind("<ButtonRelease-1>", self.on_left_mouse_action)
        self.bind("<B1-Motion>", self.on_left_mouse_action)

    def draw_line(self, s: Point, e: Point):
        self.create_line(self.canvasx(s.x), self.canvasy(s.y), self.canvasx(e.x), self.canvasy(e.y),
                         fill=self._outline_color)

    def fill_polygon(self, points: List[Point]):
        processed_points = []
        [processed_points.extend([p.x, p.y]) for p in points]
        self.create_polygon(processed_points, outline=self._outline_color, fill=self._fill_color)

    def redisplay(self):
        self.delete("all")
        for go in self._dm.get_objects():
            go.render(self)
            self._current_state.after_draw(self, go)
        self._current_state.after_draw_done(self)

    def on_key_pressed(self, event):
        if event.keysym == "Escape":
            self.set_state(IdleState())
        else:
            self._current_state.key_pressed(event)

    def is_ctrl_down(self, event):
        return (event.state & 0x4) != 0

    def is_shift_down(self, event):
        return (event.state & 0x1) != 0

    def on_left_mouse_action(self, event):
        if event.type == EventType.ButtonPress:
            self._current_state.mouse_down(Point(event.x, event.y), self.is_shift_down(event), self.is_ctrl_down(event))
        elif event.type == EventType.ButtonRelease:
            self._current_state.mouse_up(Point(event.x, event.y), self.is_shift_down(event), self.is_ctrl_down(event))
        elif event.type == EventType.Motion:
            self._current_state.mouse_dragged(Point(event.x, event.y))

    def set_state(self, state):
        print("New state:", state)
        self._current_state.on_leaving()
        self._current_state = state
