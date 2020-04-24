from __future__ import annotations

import datetime
import time
from abc import ABC, abstractmethod
from typing import List


class CollectionSubject(ABC):

    @abstractmethod
    def getCollection(self):
        pass

    @abstractmethod
    def attach(self, observer: CollectionObserver):
        pass

    @abstractmethod
    def detach(self, observer: CollectionObserver):
        pass

    @abstractmethod
    def notify(self):
        pass


class CollectionObserver(ABC):
    @abstractmethod
    def update(self, subject: CollectionSubject):
        pass


class NumberSequenceSubject(CollectionSubject):
    def __init__(self, number_source: NumberSource):
        self._collection = list()
        self._observers = set()
        self._numberSource = number_source

    @property
    def numberSource(self) -> NumberSource:
        return self._numberSource

    @numberSource.setter
    def numberSource(self, number_source: NumberSource) -> None:
        self._numberSource = number_source

    def go(self):
        print("(go entered)")
        while self._numberSource:
            x = self._numberSource.takeNext()
            if x == NumberSource.END_OF_INPUT:
                print("(End of source reached, adios!)")
                break

            if x != NumberSource.NUMBER_NOT_GENERATED_YET:
                print("(go added this value to collection: {})".format(x))
                self._add(x)
                print()

            time.sleep(1)
        print("(go left)")

    def _add(self, x):
        self._collection.append(x)
        self.notify()

    def getCollection(self) -> List:
        return self._collection

    def attach(self, observer: CollectionObserver) -> None:
        self._observers.add(observer)

    def detach(self, observer: CollectionObserver) -> None:
        self._observers.remove(observer)

    def notify(self):
        for o in self._observers:  # TODO can this for loop be hazardous
            o.update(self)


class NumberSource(ABC):
    END_OF_INPUT = -1
    NUMBER_NOT_GENERATED_YET = -2

    @abstractmethod
    def takeNext(self):
        pass


class KeyboardNumberSource(NumberSource):
    def __init__(self):
        self._numbers = []

    def takeNext(self):
        while not len(self._numbers):
            print(
                "Please enter a line of input (preferably numbers) (q or quit or to quit) (GO is now blocked and "
                "waiting; whoops):", end="")
            input_str = input()  # TODO the program will get stuck here...
            if input_str == "q" or input_str == "quit":
                return NumberSource.END_OF_INPUT
            self._numbers.extend([int(s) for s in input_str.split() if s.isdigit()][::-1])

        return self._numbers.pop()


class FileNumberSource(NumberSource):
    def __init__(self, filepath):
        with open(filepath, "r+") as file:
            self._numbers = [int(s) for s in file.read().split() if s.isdigit()][::-1]

    def takeNext(self):
        if not len(self._numbers):
            return NumberSource.END_OF_INPUT

        return self._numbers.pop()


class FileLoggerObserver(CollectionObserver):
    def __init__(self, log_filepath):
        self._log_file = open(log_filepath, "a+")
        self._log_file.write("*** FILE LOGGER SESSION STARTED ({}) ***\n".format(self._getFormattedTime()))

    @staticmethod
    def _getFormattedTime():
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def update(self, subject: CollectionSubject) -> None:
        date = self._getFormattedTime()
        state = str(subject.getCollection())
        self._log_file.write("{}:\t{}\n".format(date, state))


class AbstractPrintObserver(CollectionObserver):
    @abstractmethod
    def outputFunction(self, collection):
        pass

    def update(self, subject: CollectionSubject):
        output = self.outputFunction(subject.getCollection())
        print(output)


class PrintLengthObserver(AbstractPrintObserver):
    def outputFunction(self, collection):
        return "N: " + str(len(collection))


class PrintSumObserver(AbstractPrintObserver):
    def outputFunction(self, collection):
        return "Sum of collection: " + str(sum(collection))


class PrintMeanObserver(AbstractPrintObserver):
    def outputFunction(self, collection):
        return "Mean of collection: " + str(sum(collection) / len(collection))


class PrintMedianObserver(AbstractPrintObserver):
    def outputFunction(self, collection):
        n = len(collection)
        median = collection[n // 2] if n % 2 == 1 else (collection[n // 2] + collection[n // 2 - 1]) * 0.5
        return "Median of collection: " + str(median)


if __name__ == '__main__':
    # sources of numbers (strategies)
    fsource_filepath = "./input.txt"
    fsource = FileNumberSource(fsource_filepath)
    ksource = KeyboardNumberSource()

    # subject
    collection_subject = NumberSequenceSubject(fsource)
    # collection_subject = NumberSequenceSubject(ksource)

    # observers
    observers = [PrintLengthObserver(), FileLoggerObserver("./log.txt"), PrintSumObserver(), PrintMeanObserver(),
                 PrintMedianObserver()]

    # attach observers to subject
    for o in observers:
        collection_subject.attach(o)

    # go!
    print("MAIN: current source is the file:", fsource_filepath)
    collection_subject.go()

    print("\n\nMAIN: changing the source, looks like the first one got exhausted!\n")
    collection_subject.numberSource = ksource

    # again!
    collection_subject.go()
