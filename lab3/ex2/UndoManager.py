from __future__ import annotations

from abc import ABC, abstractmethod

from actions.edit_action import EditAction


class UndoManagerStackObserver(ABC):
    """
    Abstract class that models an UndoManager observer. The observer gets notified if undo or redo stacks go empty.
    """

    @abstractmethod
    def stack_empty(self, is_empty: bool):
        pass


class UndoManager:
    _instance = None

    def __init__(self):
        if self._instance is None:
            self._undoStack = []
            self._redoStack = []
            self._undoObservers = []
            self._redoObservers = []
            UndoManager._instance = self
        else:
            raise Exception("This class is a singleton which has already been initialized!")

    @staticmethod
    def get_instance():
        if UndoManager._instance is None:
            return UndoManager()
        else:
            return UndoManager._instance

    def is_undo_empty(self):
        return len(self._undoStack) == 0

    def is_redo_empty(self):
        return len(self._redoStack) == 0

    def attach_undo_observer(self, observer: UndoManagerStackObserver):
        """
        :param observer: observer to attach
        """
        self._undoObservers.append(observer)

    def detach_undo_observer(self, observer: UndoManagerStackObserver):
        """
        :param observer: observer to detach
        """
        self._undoObservers.remove(observer)

    def attach_redo_observer(self, observer: UndoManagerStackObserver):
        """
        :param observer: observer to attach
        """
        self._redoObservers.append(observer)

    def detach_redo_observer(self, observer: UndoManagerStackObserver):
        """
        :param observer: observer to detach
        """
        self._redoObservers.remove(observer)

    def notify_undo_empty(self, is_empty: bool):
        """
        Notify all undo observers that the undo stack is empty
        """
        for o in self._undoObservers:
            o.stack_empty(is_empty)

    def notify_redo_empty(self, is_empty: bool):
        """
        Notify all redo observers that the redo stack is empty
        """
        for o in self._redoObservers:
            o.stack_empty(is_empty)

    def undo(self):
        """
        Removes a command from the undo stack, pushes it onto the redo stack and executes.
        """
        command = self._undoStack.pop()
        self._redoStack.append(command)

        command.execute_undo()

        self.notify_undo_empty(len(self._undoStack) == 0)
        self.notify_redo_empty(len(self._redoStack) == 0)

        # if not len(self._undoStack):
        #     self.notify_undo_empty(True)
        # if len(self._redoStack) == 1:
        #     self.notify_redo_empty(False)

    def redo(self):
        command = self._redoStack.pop()
        self._undoStack.append(command)

        command.execute_do()

        self.notify_undo_empty(len(self._undoStack) == 0)
        self.notify_redo_empty(len(self._redoStack) == 0)

        # if not len(self._redoStack):
        #     self.notify_redo_empty(True)
        # if len(self._undoStack) == 1:
        #     self.notify_undo_empty(False)

    def push(self, command: EditAction):
        """
        Deletes redo stack and pushes a command onto the undo stack.
        :param command: The command to push
        """
        self._redoStack.clear()
        self._undoStack.append(command)

        self.notify_undo_empty(len(self._undoStack) == 0)
        self.notify_redo_empty(len(self._redoStack) == 0)
        # self.notify_redo_empty(True)
        # if len(self._undoStack) == 1:
        #     self.notify_redo_empty(False)

    def push_and_execute(self, command: EditAction):
        self.push(command)
        command.execute_do()
