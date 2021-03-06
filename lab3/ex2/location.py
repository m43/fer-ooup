# -*- coding: utf-8 -*-

class Location:
    def __init__(self, location=0):
        self._location = location

    def get(self):
        return self._location

    def set(self, new_location):
        self._location = new_location

    def decrease(self, delta=1):
        self._location -= delta

    def increase(self, delta=1):
        self._location += delta

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self._location)


class LocationRange:
    def __init__(self, start=0, end=0):
        self._start = Location(start)
        self._end = Location(end)

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_left(self):
        return self._start if self._start.get() <= self._end.get() else self._end

    def get_right(self):
        return self._start if self._start.get() > self._end.get() else self._end

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "(" + str(self._start) + "," + str(self._end) + ")"

    def is_empty(self):
        return self._start.get() == self._end.get()

    def clone(self):
        return LocationRange(self._start.get(), self._end.get())
