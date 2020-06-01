# -*- coding: utf-8 -*-

from __future__ import annotations

from tkinter import *
from tkinter import filedialog

from flat_colors import FlatUiColors
from geometry.composite_shape import CompositeShape
from model.document_model import DocumentModel
from painter_canvas import PainterCanvas
from states.add_shape_state import AddShapeState
from states.eraser_state import EraserState
from states.select_shape_state import SelectshapeState
from svg_renderer_impl import SvgRendererImpl


class Painter(Frame):
    def __init__(self, tools, **kw):
        super().__init__(**kw)
        self._tools = tools
        self._id_to_prototype = dict([(tool.get_shape_id(), tool) for tool in tools])
        combo_prototype = CompositeShape([])
        self._id_to_prototype[combo_prototype.get_shape_id()] = combo_prototype
        self._dm = DocumentModel()

        ## Dummy objects
        # self._dm.add_graphical_object(LineSegment(Point(10, 100), Point(20, 200)))
        # self._dm.add_graphical_object(LineSegment(Point(10, 10), Point(20, 110)))
        # self._dm.add_graphical_object(Oval(Point(30, 30), Point(45, 45)))
        # self._dm.add_graphical_object(LineSegment(Point(30, 30), Point(45, 45)))
        # self._dm.add_graphical_object(Oval(Point(100, 200), Point(200, 100)))
        # self._dm.add_graphical_object(LineSegment(Point(100, 200), Point(200, 100)))
        # self._dm.add_graphical_object(Oval())
        # self._dm.add_graphical_object(LineSegment())

        self._canvas = PainterCanvas(self._dm)
        self._canvas.redisplay()
        self._init_toolbar()

    def _init_toolbar(self):
        toolbar = Frame(self.master, bg=FlatUiColors.PETER_RIVER)

        load = Button(toolbar, text="Load", command=self.load, state=NORMAL, bg=FlatUiColors.PETER_RIVER)
        load.pack(side=LEFT, padx=2, pady=2)

        save = Button(toolbar, text="Save", command=self.save, state=NORMAL, bg=FlatUiColors.PETER_RIVER)
        save.pack(side=LEFT, padx=2, pady=2)

        svg_export = Button(toolbar, text="SVG export", command=self.export, state=NORMAL, bg=FlatUiColors.PETER_RIVER)
        svg_export.pack(side=LEFT, padx=2, pady=2)

        for tool in self._tools:
            command = lambda tool=tool: self._canvas.set_state(AddShapeState(tool, self._dm))
            tool_button = Button(toolbar, text=tool.get_shape_name(), command=command, bg=FlatUiColors.EMERALD,
                                 state=NORMAL)
            tool_button.pack(side=LEFT, padx=2, pady=2)

        select = Button(toolbar, text="Select", command=lambda: self._canvas.set_state(SelectshapeState(self._dm)),
                        state=NORMAL, bg=FlatUiColors.SUN_FLOWER)
        select.pack(side=LEFT, padx=2, pady=2)

        delete = Button(toolbar, text="Delete selection",
                        command=lambda: self._canvas.set_state(EraserState(self._dm, self._canvas)), state=NORMAL,
                        bg=FlatUiColors.ALIZARIN)
        delete.pack(side=LEFT, padx=2, pady=2)

        # UndoManager.get_instance().attach_redo_observer(
        #     type("UndoManagerStackObserver4", (UndoManagerStackObserver, object),
        #          {"stack_empty": lambda _, e: redo.config(state=DISABLED if e else NORMAL)})())
        # self._model.attach_selection_observer(
        #     type("SelectionObserverCopyTool", (SelectionObserver, object),
        #          {"update_selection": lambda _, e: copy.config(state=DISABLED if not e else NORMAL)})())
        # self._model.attach_selection_observer(
        #     type("SelectionObserverCutTool", (SelectionObserver, object),
        #          {"update_selection": lambda _, e: cut.config(state=DISABLED if not e else NORMAL)})())
        # self._clipboardStack.attach_clipboard_observer(
        #     type("ClipboardObserverPasteTool", (ClipboardObserver, object),
        #          {"update_clipboard": lambda _, e: paste.config(state=DISABLED if not e else NORMAL)})())

        toolbar.pack(side=TOP, fill=X)

    def delete_selection(self):
        pass

    def load(self):
        with filedialog.askopenfile(mode='r', defaultextension=".txt") as f:
            if f is None:
                return
            stack = []
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                l, r = line.split(maxsplit=1)
                self._id_to_prototype[l].load(stack, r)
            self._dm.clear()
            for go in stack:
                self._dm.add_graphical_object(go)

    def save(self):
        with filedialog.asksaveasfile(mode='w', defaultextension=".txt") as f:
            if f is None:
                return
            rows = []
            [go.save(rows) for go in self._dm.get_objects()]
            f.write("\n".join(rows))

    def export(self):
        with filedialog.asksaveasfile(mode='w', defaultextension=".txt") as file:
            if file is None:
                return
            r = SvgRendererImpl(file.name)
            for go in self._dm.get_objects():
                go.render(r)
            r.save_and_close()
