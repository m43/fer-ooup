# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod

from UndoManager import UndoManager
from clipboard import ClipboardStack
from text_editor_model import TextEditorModel
from tkinter import messagebox


class StatisticsPlugin(ABC):
    def get_name(self) -> str:
        return "stat"

    @abstractmethod
    def get_description(self) -> str:
        return "stat. desc."

    @abstractmethod
    def execute(self, model: TextEditorModel, um: UndoManager, clipboard_stack: ClipboardStack) -> None:
        lines = list(model.all_lines())
        lines_count = len(lines)
        words_count = len("\n".join(lines).split())
        letter_count = len("".join("\n".join(lines).split()))
        messagebox.showinfo("Statistika", "lines {} words {} letters {}".format(lines_count, words_count, letter_count))
