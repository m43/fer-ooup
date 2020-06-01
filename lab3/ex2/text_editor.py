# -*- coding: utf-8 -*-

from __future__ import annotations

import importlib.util
import inspect
import os
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font

import flat_colors
from UndoManager import UndoManager, UndoManagerStackObserver
from clipboard import ClipboardStack, ClipboardObserver
from plugin import Plugin
from text_editor_model import *


class TextEditor(Frame, CaretObserver, TextObserver):
    def update_text(self, text: str):
        self.update_status_bar()
        self.redisplay()

    def update_caret_location(self, loc: Location):
        self.update_status_bar()
        self.redisplay()

    def __init__(self, text_editor_model: TextEditorModel):
        super().__init__()

        # TODO extract
        self._minimalWidth = 555
        self._minimalHeight = 700
        self._xMargin = 10
        self._numberSpacing = 50
        self._yMargin = 20
        self._font = Font(size=12, family="Purisa")
        self._canvasTextColor = flat_colors.FlatUiColors.CLOUDS
        self._canvasBackgroundColor = flat_colors.FlatUiColors.PETER_RIVER
        self._canvasHighlightColor = flat_colors.FlatUiColors.EMERALD

        # TODO extract
        self._caretShownDelay = 300
        self._caretHiddenDelay = 5000
        self._caretColor = flat_colors.FlatUiColors.MIDNIGHT_BLUE

        self.__processed_selection = []

        self._model = text_editor_model
        self._model._caretObservers.add(self)
        # using an anonymous class:
        # self._model._observers.add(type("Pero", (CaretObserver, object),
        #                                 {"updateCaretLocation": lambda _, __: self.redisplay()})())

        self._clipboardStack = ClipboardStack()

        self._pluginsDirectory = "./plugins/"
        self._pluginsModuleName = "plugins"
        self._plugins = self._load_plugins()

        self.init_menubar()
        self.init_toolbar()
        self.init_statusbar()
        self.init_canvas()

    def _load_plugins(self):
        plugins = []
        for file in os.listdir(self._pluginsDirectory):
            if file.endswith(".py"):
                print(file)
                # try:
                spec = importlib.util.spec_from_file_location(
                    self._pluginsModuleName, self._pluginsDirectory + file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, obj in inspect.getmembers(
                        module, lambda x: inspect.isclass(x) and issubclass(x, Plugin) and not inspect.isabstract(x)):
                    plugins.append(obj())
                # except:
                #     pass

        return plugins

    def init_menubar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label="Open", underline=0, command=self.open_file)
        file_menu.add_command(label="Save", underline=0, command=self.save_file)
        file_menu.add_command(label="Exit", underline=0, command=self.on_exit)
        menubar.add_cascade(label="File", underline=0, menu=file_menu)

        edit_menu = Menu(menubar)
        edit_menu.add_command(label="Undo", command=self.undo, state=DISABLED)
        UndoManager.get_instance().attach_undo_observer(
            type("UndoManagerStackObserver1", (UndoManagerStackObserver, object),
                 {"stack_empty": lambda _, e: edit_menu.entryconfig(1, state=DISABLED if e else NORMAL)})())

        edit_menu.add_command(label="Redo", command=self.redo, state=DISABLED)
        UndoManager.get_instance().attach_redo_observer(
            type("UndoManagerStackObserver2", (UndoManagerStackObserver, object),
                 {"stack_empty": lambda _, e: edit_menu.entryconfig(2, state=DISABLED if e else NORMAL)})())

        edit_menu.add_command(label="Cut", command=self.cut, state=DISABLED)
        self._model.attach_selection_observer(
            type("SelectionObserverCut", (SelectionObserver, object),
                 {"update_selection": lambda _, e: edit_menu.entryconfig(3, state=DISABLED if not e else NORMAL)})())

        edit_menu.add_command(label="Copy", command=self.copy, state=DISABLED)
        self._model.attach_selection_observer(
            type("SelectionObserverCopy", (SelectionObserver, object),
                 {"update_selection": lambda _, e: edit_menu.entryconfig(4, state=DISABLED if not e else NORMAL)})())

        edit_menu.add_command(label="Paste", command=self.paste, state=DISABLED)
        self._clipboardStack.attach_clipboard_observer(
            type("ClipboardObserverPaste", (ClipboardObserver, object),
                 {"update_clipboard": lambda _, e: edit_menu.entryconfig(5, state=DISABLED if not e else NORMAL)})())

        edit_menu.add_command(label="Paste and Take", command=self.paste_and_take)
        self._clipboardStack.attach_clipboard_observer(
            type("ClipboardObserverPasteAndTake", (ClipboardObserver, object),
                 {"update_clipboard": lambda _, e: edit_menu.entryconfig(6, state=DISABLED if not e else NORMAL)})())

        edit_menu.add_command(label="Delete selection", command=self.delete_selection, state=DISABLED)
        self._model.attach_selection_observer(
            type("SelectionObserverDelete", (SelectionObserver, object),
                 {"update_selection": lambda _, e: edit_menu.entryconfig(7, state=DISABLED if not e else NORMAL)})())

        edit_menu.add_command(label="Clear document", command=self.clear_document)
        menubar.add_cascade(label="Edit", underline=0, menu=edit_menu)

        move_menu = Menu(menubar)
        move_menu.add_command(label="Caret to document start", command=self.caret_to_start)
        move_menu.add_command(label="Caret to document end", command=self.caret_to_end)
        menubar.add_cascade(label="Move", underline=0, menu=move_menu)

        plugins_menu = Menu(menubar)
        for plugin in self._plugins:
            plugins_menu.add_command(
                label=plugin.get_name(),
                command=lambda p=plugin: p.execute(self._model, UndoManager.get_instance(), self._clipboardStack))

        menubar.add_cascade(label="Plugins", underline=0, menu=plugins_menu)

    def init_toolbar(self):
        toolbar = Frame(self.master)

        undo = Button(toolbar, text="Undo", command=self.undo, state=DISABLED)
        undo.pack(side=LEFT, padx=2, pady=2)
        UndoManager.get_instance().attach_undo_observer(
            type("UndoManagerStackObserver3", (UndoManagerStackObserver, object),
                 {"stack_empty": lambda _, e: undo.config(state=DISABLED if e else NORMAL)})())

        redo = Button(toolbar, text="Redo", command=self.redo, state=DISABLED)
        redo.pack(side=LEFT, padx=2, pady=2)
        UndoManager.get_instance().attach_redo_observer(
            type("UndoManagerStackObserver4", (UndoManagerStackObserver, object),
                 {"stack_empty": lambda _, e: redo.config(state=DISABLED if e else NORMAL)})())

        copy = Button(toolbar, text="Copy", command=self.copy, state=DISABLED)
        copy.pack(side=LEFT, padx=2, pady=2)
        self._model.attach_selection_observer(
            type("SelectionObserverCopyTool", (SelectionObserver, object),
                 {"update_selection": lambda _, e: copy.config(state=DISABLED if not e else NORMAL)})())

        cut = Button(toolbar, text="Cut", command=self.cut, state=DISABLED)
        cut.pack(side=LEFT, padx=2, pady=2)
        self._model.attach_selection_observer(
            type("SelectionObserverCutTool", (SelectionObserver, object),
                 {"update_selection": lambda _, e: cut.config(state=DISABLED if not e else NORMAL)})())

        paste = Button(toolbar, text="Paste", command=self.cut, state=DISABLED)
        paste.pack(side=LEFT, padx=2, pady=2)
        self._clipboardStack.attach_clipboard_observer(
            type("ClipboardObserverPasteTool", (ClipboardObserver, object),
                 {"update_clipboard": lambda _, e: paste.config(state=DISABLED if not e else NORMAL)})())

        toolbar.pack(side=TOP, fill=X)

    def init_statusbar(self):
        self._statusbar = Label(self.master, bd=1, relief=SUNKEN, padx=6, pady=4, anchor=E)
        self._statusbar.pack(side=BOTTOM, fill=X)
        self.update_status_bar()

    def init_canvas(self):
        self.master.title("Lab 3 example")
        self.pack(fill=BOTH, expand=1)

        self._display_caret = True
        self._selecting_active = False
        self._canvas = Canvas(self, bg=self._canvasBackgroundColor,
                              scrollregion=(0, 0, self._minimalWidth, self._minimalHeight))
        self._vbar = Scrollbar(self, orient=VERTICAL)
        self._vbar.pack(side=RIGHT, fill=Y)
        self._vbar.config(command=self._canvas.yview)
        self._hbar = Scrollbar(self, orient=HORIZONTAL)
        self._hbar.pack(side=BOTTOM, fill=X)
        self._hbar.config(command=self._canvas.xview)
        self._canvas.config(xscrollcommand=self._hbar.set, yscrollcommand=self._vbar.set)
        self._canvas.pack(fill=BOTH, expand=1)

        self.redisplay()
        self._canvas.bind_all("<Key>", self.on_key_pressed)
        self._other_dialog_open = False
        self.after(self._caretShownDelay, self.on_timer)

    def redisplay(self, update_selection=False):
        # print("caret loc", self._model.get_caret_location().get(), "||| current row and column",
        #       self._model.find_caret(), "|||| sel", self._model.get_selection_range().get_start(),
        #       self._model.get_selection_range().get_end())
        row_height = self._font.metrics()["linespace"]
        (caret_row, caret_column) = self._model.find_caret()

        height = max(self._minimalHeight, len(
            list(self._model.all_lines())) * row_height + 2 * self._yMargin)
        width = max(self._minimalWidth, self._font.measure(
            max(list(self._model.all_lines()), key=len)) + self._numberSpacing + 2 * self._xMargin)
        self._canvas.delete("all")
        self._canvas.config(scrollregion=(0, 0, width, height))

        # TODO follow caret by scrolling left/right and up/down
        # deltaX =
        # deltaY =

        self._render_selection(update_selection)
        self._render_caret(caret_row, caret_column)

        for (i, line) in enumerate(self._model.all_lines()):
            self._canvas.create_text(self._xMargin, self._yMargin + row_height * i, font=self._font, text=str(i),
                                     anchor=NW, fill=self._canvasTextColor)
            self._canvas.create_text(self._xMargin + self._numberSpacing, self._yMargin + row_height * i,
                                     font=self._font, text=line, anchor=NW, fill=self._canvasTextColor)

    def update_selection(self, right_end_moved: bool):
        """
        Update the current selection in the TextEditorModel. If selecting is inactive, the selection will be reset to
        range [current_caret_location, current_caret_location]. Otherwise, the range will be updated in accordance with
        the new caret position.
        :param right_end_moved: was the caret at the right end of the selection
        """
        # TODO move to an more appropriate place
        new_caret_location = self._model.get_caret_location().get()
        if self._selecting_active:
            selection_before = self._model.get_selection_range()
            if right_end_moved:
                self._model.set_selection_range(LocationRange(selection_before.get_start().get(), new_caret_location))
            else:
                self._model.set_selection_range(LocationRange(new_caret_location, selection_before.get_end().get()))
        else:
            self._model.reset_selection()

    def on_timer(self):
        self._display_caret = not self._display_caret
        self.redisplay(True)
        self.after(self._caretShownDelay if not self._display_caret else self._caretShownDelay, self.on_timer)

    def on_exit(self):
        self.master.destroy()

    def get_x_y_of_line_start(self, row):
        return self._xMargin + self._numberSpacing, self._yMargin + self._font.metrics()["linespace"] * row

    def get_x_y_of_line_end(self, row):
        return (self._xMargin + self._numberSpacing + self._font.measure(self._model.get_line(row)),
                self._yMargin + self._font.metrics()["linespace"] * row)

    def get_x_y_at_caret_location(self, caret_location: Location):
        row, column = self._model.find_location(caret_location)
        return self.get_x_y_at_row_and_column(row, column)

    def get_x_y_at_row_and_column(self, row, column):
        xy_tuple = self.get_x_y_of_line_start(row)
        x, y = xy_tuple[0], xy_tuple[1]
        return x + self._font.measure(self._model.get_line(row)[:column]), y

    def row_height(self):
        return self._font.metrics()["linespace"]

    def _render_caret(self, caret_row, caret_column):
        color = self._caretColor if self._display_caret else self._canvasBackgroundColor
        x_start = self._xMargin + self._numberSpacing + self._font.measure(
            self._model.get_line(caret_row)[:caret_column])
        y_start = self._yMargin + self.row_height() * caret_row + 3
        self._canvas.create_line(x_start - 3, y_start, x_start + 3, y_start, fill=color)
        self._canvas.create_line(x_start, y_start, x_start, y_start + self._font.metrics()["linespace"] - 9, fill=color)
        self._canvas.create_line(x_start - 3, y_start + self._font.metrics()["linespace"] - 9, x_start + 3,
                                 y_start + self._font.metrics()["linespace"] - 9, fill=color)

    def _render_selection(self, update_selection=True):
        selection = self._model.get_selection_range()
        if selection.get_start().get() == selection.get_end().get():
            return

        if update_selection:
            self.__preprocess_selection(selection)

        for e in self.__processed_selection:
            self._canvas.create_rectangle(e[0][0], e[0][1], e[1][0], e[1][1] + self.row_height(),
                                          outline=self._canvasHighlightColor, fill=self._canvasHighlightColor)

    def __preprocess_selection(self, selection: LocationRange):
        sel_start_r, sel_start_c = self._model.find_location(selection.get_start())
        sel_end_r, sel_end_c = self._model.find_location(selection.get_end())

        if sel_start_r > sel_end_r or sel_start_r == sel_end_r and sel_start_c > sel_end_c:
            sel_start_r, sel_start_c, sel_end_r, sel_end_c = sel_end_r, sel_end_c, sel_start_r, sel_start_c

        if sel_start_r == sel_end_r:
            self.__processed_selection = [(self.get_x_y_at_row_and_column(sel_start_r, sel_start_c),
                                           self.get_x_y_at_row_and_column(sel_end_r, sel_end_c))]
        else:
            self.__processed_selection = [(self.get_x_y_at_row_and_column(sel_start_r, sel_start_c),
                                           self.get_x_y_of_line_end(sel_start_r))]
            self.__processed_selection += [(self.get_x_y_of_line_start(row), self.get_x_y_of_line_end(row)) for row in
                                           range(sel_start_r + 1, sel_end_r)]
            self.__processed_selection += [(self.get_x_y_of_line_start(sel_end_r),
                                            self.get_x_y_at_row_and_column(sel_end_r, sel_end_c))]

    def update_status_bar(self):
        ln, col = self._model.find_caret()
        total_rows = self._model.get_lines_count()
        self._statusbar['text'] = "Ln: {}, Col: {}\tTotal rows: {}".format(ln, col, total_rows)

    def on_key_pressed(self, e):
        if self._other_dialog_open:
            return
        keysym = e.keysym
        char = e.char

        # https://stackoverflow.com/questions/19861689/check-if-modifier-key-is-pressed-in-tkinter
        ctrl = (e.state & 0x4) != 0
        alt = (e.state & 0x8) != 0 or (e.state & 0x80) != 0
        shift = (e.state & 0x1) != 0
        self._selecting_active = shift

        # print(e.keysym, e.char, e.keycode, e.char.isprintable(), "%x" % e.state, ctrl, shift, alt)

        if keysym == "Left":
            self._display_caret = True
            caret_before = self._model.get_caret_location().get()
            self._model.move_caret_left()
            self.update_selection(caret_before == self._model.get_selection_range().get_end().get())
        elif keysym == "Right":
            self._display_caret = True
            caret_before = self._model.get_caret_location().get()
            self._model.move_caret_right()
            self.update_selection(caret_before == self._model.get_selection_range().get_end().get())
        elif keysym == "Up":
            self._display_caret = True
            caret_before = self._model.get_caret_location().get()
            self._model.move_caret_up()
            self.update_selection(caret_before == self._model.get_selection_range().get_end().get())
        elif keysym == "Down":
            self._display_caret = True
            caret_before = self._model.get_caret_location().get()
            self._model.move_caret_down()
            self.update_selection(caret_before == self._model.get_selection_range().get_end().get())
        elif keysym == "BackSpace":
            self._display_caret = True
            if self._model.get_selection_range().is_empty():
                action = self._model.execute_delete_before()
                if action is not None:
                    UndoManager.get_instance().push(action)
            else:
                self.delete_selection()
        elif keysym == "Delete":
            self._display_caret = True
            if self._model.get_selection_range().is_empty():
                action = self._model.execute_delete_after()
                if action is not None:
                    UndoManager.get_instance().push(action)
            else:
                self.delete_selection()
        elif keysym == "Return":
            # TODO what if None
            action1 = self.delete_selection(False)
            action2 = self._model.execute_insert_at_caret("\n")
            actions = [a for a in [action1, action2] if a is not None]
            if actions:
                UndoManager.get_instance().push(JumboEditAction(actions))
        elif keysym == "Escape":
            self._display_caret = True
            self.master.destroy()
        elif ctrl and keysym.lower() == "c":
            self.copy()
        elif ctrl and keysym.lower() == "x":
            self.cut()
        elif ctrl and keysym.lower() == "v":
            if shift:
                self.paste_and_take()
            else:
                self.paste()
        elif ctrl and keysym.lower() == "y":
            self.redo()
        elif ctrl and keysym.lower() == "z":
            self.undo()
        elif len(char) and char.isprintable():
            # TODO should LocationRange be immutable? Or how should I pass it around?
            action1 = self.delete_selection(False)
            action2 = self._model.execute_insert_at_caret(char)
            self._model.reset_selection()
            actions = [a for a in [action1, action2] if a is not None]
            if actions:
                UndoManager.get_instance().push(JumboEditAction(actions))

    def open_file(self):
        self._other_dialog_open = True
        try:
            f = filedialog.askopenfile(mode='r', defaultextension=".txt")
            if f is None:
                return
            text = "\n".join(f.readlines())
            self._model.set_text(text)
            f.close()
        finally:
            self._other_dialog_open = False

    def save_file(self):
        self._other_dialog_open = True
        try:
            f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
            if f is None:
                return
            text = "\n".join(self._model.all_lines())
            f.write(text)
            f.close()
        finally:
            self._other_dialog_open = False

    def undo(self):
        um = UndoManager.get_instance()
        if not um.is_undo_empty():
            um.undo()

    def redo(self):
        um = UndoManager.get_instance()
        if not um.is_redo_empty():
            um.redo()

    def copy(self):
        if not self._model.get_selection_range().is_empty():
            self._clipboardStack.push(self._model.get_selected_text())

    def cut(self):
        if not self._model.get_selection_range().is_empty():
            self._clipboardStack.push(self._model.get_selected_text())
            self.delete_selection()

    def paste(self):
        if self._clipboardStack.has_any():
            self.delete_selection()
            action = self._model.execute_insert_at_caret(self._clipboardStack.peek())
            if action is not None:
                UndoManager.get_instance().push(action)

    def paste_and_take(self):
        if self._clipboardStack.has_any():
            action1 = self.delete_selection(False)
            action2 = self._model.execute_insert_at_caret(self._clipboardStack.pop())
            actions = [a for a in [action1, action2] if a is not None]
            if actions:
                UndoManager.get_instance().push(JumboEditAction(actions))

    def delete_selection(self, push_action=True) -> EditAction:
        if self._model.get_selection_range().is_empty():
            return
        sel_left = self._model.get_selection_range().get_left()
        self._model.move_caret_to(sel_left)

        action = self._model.execute_delete_range(self._model.get_selection_range().clone())
        if push_action and action is not None:
            UndoManager.get_instance().push(action)
        self._model.set_selection_range(LocationRange(sel_left.get(), sel_left.get()))
        return action

    def clear_document(self):
        self._model.set_selection_range(LocationRange(0, self._model.get_caret_max()))
        self.delete_selection()

    def caret_to_start(self):
        self._model.move_caret_to(Location(0))

    def caret_to_end(self):
        self._model.move_caret_to(Location(self._model.get_caret_max()))
