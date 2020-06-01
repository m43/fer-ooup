# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod


class ClipboardStack:
    def __init__(self):
        self._texts = []  # stack
        self._clipboardObservers = set()

    def push(self, text):
        """
        Push given text onto clipboard stack of texts
        :param text: text to push
        """
        self._texts.append(text)
        self.notify_clipboard_observers()

    def pop(self):
        """
        Pop last text from clipboard stack of texts
        :return: popped text
        """
        if not len(self._texts):
            raise ValueError("Clipboard stack is empty.")
        result = self._texts.pop()
        self.notify_clipboard_observers()
        return result

    def has_any(self):
        """
        :return: True if clipboard stack of texts contains any text
        """
        return len(self._texts) != 0

    def peek(self):
        """
        :return: Peek the topmost text of the clipboard stack of texts
        """
        if not len(self._texts):
            raise ValueError("Clipboard stack is empty.")
        return self._texts[-1]

    def empty(self):
        """
        Empty the clipboard stack of texts
        """
        self._texts.clear()
        self.notify_clipboard_observers()

    def attach_clipboard_observer(self, observer: ClipboardObserver):
        """
        :param observer: observer to attach
        """
        self._clipboardObservers.add(observer)

    def detach_clipboard_observer(self, observer: ClipboardObserver):
        """
        :param observer: observer to detach
        """
        self._clipboardObservers.remove(observer)

    def detach_all_clipboard_observers(self):
        """
        Detaches any clipboard observer
        """
        self._clipboardObservers.clear()

    def notify_clipboard_observers(self):
        """
        Call to notify all clipboard observers about the the clipboard update
        """
        for o in self._clipboardObservers:
            o.update_clipboard(self.has_any())


class ClipboardObserver(ABC):
    """
    Class models an clipboard observer. Every observer gets notified if clipboard gets changed.
    """

    @abstractmethod
    def update_clipboard(self, has_any):
        """
        Method gets called when observed clipboard is updated.
        """
        pass
