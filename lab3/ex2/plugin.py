# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod

from UndoManager import UndoManager
from clipboard import ClipboardStack
from text_editor_model import TextEditorModel


class Plugin(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def execute(self, model: TextEditorModel, um: UndoManager, clipboard_stack: ClipboardStack) -> None:
        pass

