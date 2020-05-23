# -*- coding: utf-8 -*-
from __future__ import annotations

from tkinter import messagebox

from UndoManager import UndoManager
from clipboard import ClipboardStack
from plugin import Plugin
from text_editor_model import TextEditorModel


class StatisticsPlugin(Plugin):
    def get_name(self) -> str:
        return "stat"

    def get_description(self) -> str:
        return "stat. desc."

    def execute(self, model: TextEditorModel, um: UndoManager, clipboard_stack: ClipboardStack) -> None:
        lines = list(model.all_lines())
        lines_count = len(lines)
        words_count = len("\n".join(lines).split())
        letter_count = len("".join("\n".join(lines).split()))
        messagebox.showinfo(
            "Statistics",
            "Lines {}\nWords {}\nLetters (without spaces) {}".format(lines_count, words_count, letter_count))
