# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod

from actions.edit_action import EditAction
from iterator import Iterator
from location import *


class ListItearator(Iterator):

    def __init__(self, some_list):
        self._list = some_list
        self._currentIdx = 0
        self._n = len(some_list)

    def __iter__(self):
        return self

    def __next__(self):
        if (self._currentIdx >= self._n):
            raise StopIteration
        self._currentIdx += 1
        return self._list[self._currentIdx - 1]


class TextObserver(ABC):
    @abstractmethod
    def update_text(self, text: str):
        pass


class CaretObserver(ABC):
    @abstractmethod
    def update_caret_location(self, loc: Location):
        pass


class SelectionObserver(ABC):
    @abstractmethod
    def update_selection(self, selection_exists: bool):
        pass


class TextEditorModel:
    """
    Class encapsulates the model of the an simple text editor with caret position, text selection
    TODO ...
    """

    def __init__(self, text):
        self._lines = text.splitlines()
        self._caretLocation = Location(0)
        self._selectionRange = LocationRange(0, 0)
        self._caretObservers = set()
        self._textObservers = set()
        self._selectionObservers = set()

    def get_caret_location(self) -> Location:
        """
        :return: the caret location
        """
        return self._caretLocation

    def get_line(self, row):
        """
        :param row: index of line to fetch, starting from 0
        :return: the line at given index
        """
        return self._lines[row]

    def all_lines(self) -> Iterator:
        """
        :return: an iterator of all lines
        """
        return ListItearator(self._lines)

    def get_lines_count(self) -> int:
        """
        :return: number of lines
        """
        return len(self._lines)

    def lines_range(self, idx1, idx2) -> Iterator:
        """
        Return an iterator of all lines from range given by [idx1, idx2)

        :param idx1: start index, included in range
        :param idx2: end index, excluded from range
        :return: an iterator of lines range
        """
        return ListItearator(self._lines[idx1, idx2])

    def attach_caret_observer(self, observer: CaretObserver):
        """
        :param observer: observer to attach
        """
        self._caretObservers.add(observer)

    def detach_caret_observer(self, observer: CaretObserver):
        """
        :param observer: observer to detach
        """
        self._caretObservers.remove(observer)

    def detach_all_caret_observers(self):
        """
        Detaches any caret observer
        """
        self._caretObservers.clear()

    def notify_caret_observers(self):
        """
        Call to notify all caret observers about the caret location update
        """
        for o in self._caretObservers:
            o.update_caret_location(self._caretLocation)

    def move_caret_left(self):
        if self._caretLocation.get() > 0:
            self._caretLocation.decrease()
            self.notify_caret_observers()

    def move_caret_right(self):
        if self._caretLocation.get() + 1 <= self.get_caret_max():
            self._caretLocation.increase()
            self.notify_caret_observers()

    def move_caret_up(self):
        current_row, current_column = self.find_caret()
        if current_row != 0:
            previous_line_length = len(self._lines[current_row - 1])
            self._caretLocation.decrease(current_column)
            self._caretLocation.decrease(previous_line_length + 1)
            self._caretLocation.increase(min(current_column, previous_line_length))
            self.notify_caret_observers()

    def move_caret_down(self):
        current_row, current_column = self.find_caret()
        if current_row != len(self._lines) - 1:
            self._caretLocation.decrease(current_column)
            self._caretLocation.increase(len(self._lines[current_row]) + 1)
            self._caretLocation.increase(min(current_column, len(self._lines[current_row + 1])))
            self.notify_caret_observers()

    def find_location(self, loc: Location):
        current_row = 0
        current_column = loc.get()
        row_lengths = [len(line) for line in self._lines]
        for row_length in row_lengths:
            if current_column > row_length:
                current_column -= row_length + 1
                current_row += 1
            else:
                return (current_row, current_column)

        # Reaching this means that the caret is after the last char of the last line.
        return (len(self._lines) - 1, len(self._lines[-1]))

    def find_caret(self):
        return self.find_location(self._caretLocation)

    def attach_text_observer(self, observer: TextObserver):
        self._textObservers.add(observer)

    def detach_text_observer(self, observer: TextObserver):
        self._textObservers.remove(observer)

    def detach_all_text_observers(self):
        self._textObservers.clear()

    def notify_text_observers(self):
        for o in self._textObservers:
            o.update_caret_location(self._caretLocation)

    def attach_selection_observer(self, observer: SelectionObserver):
        """
        :param observer: observer to attach
        """
        self._selectionObservers.add(observer)

    def detach_selection_observer(self, observer: SelectionObserver):
        """
        :param observer: observer to detach
        """
        self._selectionObservers.remove(observer)

    def notify_selection_observers(self):
        """
        Call to notify all observers
        """
        for o in self._selectionObservers:
            o.update_selection(not self.get_selection_range().is_empty())

    def execute_delete_before(self) -> EditAction:
        # TODO refactor - move action creation somewhere else!
        if self._caretLocation.get() != 0:
            caret = self._caretLocation.get()
            action = GeneralEditAction(self, LocationRange(caret - 1, caret), "")
            action.execute_do()
            # row, column = self.find_caret()
            # if column == 0:
            #     self._lines[row - 1] += self._lines[row]
            #     del (self._lines[row])
            # else:
            #     self._lines[row] = self._lines[row][:column - 1] + self._lines[row][column:]
            self.get_caret_location().decrease()
            self.notify_text_observers()
            self.notify_caret_observers()
            return action

    def execute_delete_after(self) -> EditAction:
        # TODO refactor - move action creation somewhere else!
        row, column = self.find_caret()
        if row != len(self._lines) - 1 or column != len(self._lines[row]):
            caret = self._caretLocation.get()
            action = GeneralEditAction(self, LocationRange(caret, caret + 1), "")
            action.execute_do()
            # if column == len(self._lines[row]):
            #     self._lines[row] += self._lines[row + 1]
            #     del (self._lines[row + 1])
            # else:
            #     self._lines[row] = self._lines[row][:column] + self._lines[row][column + 1:]
            self.notify_text_observers()
            self.notify_caret_observers()
            return action

    def execute_delete_range(self, r: LocationRange):
        action = GeneralEditAction(self, r, "")
        action.execute_do()
        return action

    def delete_range(self, r: LocationRange):
        """
        Deletes the given text range from lines.
        :param r: range to delete
        """
        l_row, l_col = self.find_location(r.get_left())
        r_row, r_col = self.find_location(r.get_right())

        self._lines[l_row] = self._lines[l_row][:l_col] + self._lines[r_row][r_col:]
        del (self._lines[l_row + 1:r_row + 1])
        self.notify_text_observers()

    def get_selection_range(self) -> LocationRange:
        """
        Returns the selection range.
        """
        return self._selectionRange

    def set_selection_range(self, r: LocationRange):
        """
        Set the current selection to given range.
        :param r: the range to set as selection
        """
        self._selectionRange = r
        self.notify_selection_observers()

    def move_caret_to(self, loc: Location):
        self._caretLocation = loc
        self.notify_caret_observers()

    def execute_insert_at_caret(self, string: str) -> EditAction:
        # TODO refactor - move action creation somewhere else!
        if not len(string):
            return

        action = self.execute_insert(string, self._caretLocation)
        self._caretLocation.increase(len(string))
        self.notify_caret_observers()
        return action

    def execute_insert(self, string: str, loc: Location) -> EditAction:
        # TODO refactor - move action creation somewhere else!
        if not len(string):
            return

        row, column = self.find_location(loc)
        current_row = self._lines[row]
        lines = string.split("\n")
        lines[0] = current_row[:column] + lines[0]
        lines[-1] = lines[-1] + current_row[column:]
        self._lines[row:row + 1] = lines

        self.notify_text_observers()

        return InsertEditAction(self, LocationRange(loc.get(), loc.get()), string)

    def get_caret_max(self):
        return sum([len(line) + 1 for line in self._lines]) - 1

    def get_text_at_range(self, range: LocationRange):
        return "\n".join(self._lines)[range.get_left().get():range.get_right().get()]

    def get_selected_text(self) -> str:
        return self.get_text_at_range(self._selectionRange)

    def reset_selection(self):
        caret = self._caretLocation.get()
        self._selectionRange = LocationRange(caret, caret)
        self.notify_selection_observers()

    def set_text(self, text):
        self._lines = text.splitlines()
        self._caretLocation = Location(0)
        self.notify_selection_observers()
        self._selectionRange = LocationRange(0, 0)
        self.notify_text_observers()


class InsertEditAction(EditAction):

    def __init__(self, model: TextEditorModel, range: LocationRange, text_to_add: str):
        self._model = model
        self._range = range
        self._textToAdd = text_to_add

    def execute_do(self):
        self._model.execute_insert(self._textToAdd, self._range.get_left())

    def execute_undo(self):
        self._model.delete_range(
            LocationRange(self._range.get_left().get(), self._range.get_left().get() + len(self._textToAdd)))


class GeneralEditAction(EditAction):

    def __init__(self, model: TextEditorModel, range: LocationRange, text_to_add: str):
        self._model = model
        self._range = range
        self._textToAdd = text_to_add
        self._deletedText = None

    def execute_do(self):
        self._deletedText = self._model.get_text_at_range(self._range)
        self._model.delete_range(self._range)
        self._model.execute_insert(self._textToAdd, self._range.get_left())

    def execute_undo(self):
        if self._deletedText is None:
            raise Exception("Cannot undo if nothing was done. First call execute_do!")
        self._model.delete_range(
            LocationRange(self._range.get_left().get(), self._range.get_left().get() + len(self._textToAdd)))
        self._model.execute_insert(self._deletedText, self._range.get_left())


class JumboEditAction(EditAction):

    def __init__(self, commands_ordered_by_execution):
        self._commands = commands_ordered_by_execution

    def execute_do(self):
        for command in self._commands:
            command.execute_do()

    def execute_undo(self):
        for command in reversed(self._commands):
            command.execute_undo()
