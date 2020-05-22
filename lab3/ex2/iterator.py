# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Iterator(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass