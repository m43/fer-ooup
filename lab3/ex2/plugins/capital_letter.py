# -*- coding: utf-8 -*-
from __future__ import annotations

from tkinter import messagebox

from UndoManager import UndoManager
from clipboard import ClipboardStack
from plugin import Plugin
from text_editor_model import TextEditorModel


class CapitalLetter(Plugin):
    def get_name(self) -> str:
        return "capital letter"

    def get_description(self) -> str:
        return "Goes through the document and makes the first letter of each word a capital letter."

    def execute(self, model: TextEditorModel, um: UndoManager, clipboard_stack: ClipboardStack) -> None:
        new_lines = [" ".join([x.capitalize() for x in line.split(" ")]) for line in model.all_lines()]

        model.set_text("\n".join(new_lines))
        messagebox.showinfo("Capital letter", "Done! Enjoy Your capital letters")
