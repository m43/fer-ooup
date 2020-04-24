from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import types
from random import normalvariate
import math


# The strategy for distribution generation
class DistributionGenerator(ABC):
    @abstractmethod
    def getElements(self):
        pass


# The strategy for percentile calculation
class PercentileCalculator(ABC):
    @abstractmethod
    def determine_percentiles(self, data: List, n_percentiles: int):
        pass


class DistributionTester:

    def __init__(self, generator: DistributionGenerator, percentile_calculator: PercentileCalculator):
        self._generator = generator
        self._percentileCalculator = percentile_calculator

    @property
    def generator(self) -> DistributionGenerator:
        return self._generator

    @generator.setter
    def generator(self, generator: DistributionGenerator) -> None:
        self._generator = generator

    @property
    def percentileCalculator(self) -> PercentileCalculator:
        return self._percentileCalculator

    @percentileCalculator.setter
    def percentileCalculator(self, percentile_calculator: PercentileCalculator) -> None:
        self._percentileCalculator = percentile_calculator

    def test(self, n_percentiles):
        data = self._generator.getElements()
        percentiles = self._percentileCalculator.determine_percentiles(data, n_percentiles)

        print("Got data:", data)
        print("Percentiles are:")
        for i in range(n_percentiles):
            percentile = 100 * (i + 1) / n_percentiles
            print("\t{} --> {:.2f}".format(percentile, percentiles[i]))
        print()


# Concrete strategy implementation
class StepByStepDistributionGenerator(DistributionGenerator):

    def __init__(self, start, end, step):  # TODO is -> None needed?
        assert end > start, "End must be greater than start"
        assert end - start >= step, "Step is too big"

        self._start = start
        self._end = end
        self._step = step

    def getElements(self) -> List:
        result = list()  # TODO how to properly use List?

        i = self._start
        while i <= self._end:
            result.append(i)
            i += self._step

        return result


# Concrete strategy implementation
class FibonacciDistributionGenerator(DistributionGenerator):
    def __init__(self, n_elements: int):
        self._n_elements = n_elements

    def getElements(self) -> List:
        result = list()

        a = 0
        b = 1
        for i in range(self._n_elements):
            result.append(a)
            a, b = b, a + b

        return result


# Concrete strategy implementation
class NormalDistributionGenerator(DistributionGenerator):
    def __init__(self, mean, sigma, n_elements: int):
        self._mean = mean
        self._sigma = sigma
        self._n_elements = n_elements

    def getElements(self) -> List:
        result = list()

        for i in range(self._n_elements):
            result.append(normalvariate(self._mean, self._sigma))

        return result


# Concrete strategy implementation
class NearestRankPercentileCalculator(PercentileCalculator):

    def __init__(self):
        pass

    def determine_percentiles(self, data: List, n_percentiles: int) -> List:
        assert n_percentiles > 0, "Number of percentiles must be positive"

        result = list()

        sorted_data = sorted(data)
        for i in range(1, n_percentiles + 1):
            percentile_position = (i / n_percentiles) * len(data)
            position = math.ceil(percentile_position)
            result.append(sorted_data[position - 1])

        return result


# Concrete strategy implementation
class LinearInterpolationPercentileCalculator(PercentileCalculator):

    def __init__(self):
        pass

    def determine_percentiles(self, data: List, n_percentiles: int) -> List:
        assert n_percentiles > 0, "Number of percentiles must be positive"

        result = list()

        sorted_data = sorted(data)
        for i in range(1, n_percentiles + 1):
            percentile = (i / n_percentiles)
            percentile_position = percentile * (len(data) - 1)

            lower_index = math.floor(percentile_position)
            upper_index = math.ceil(percentile_position)
            lower = sorted_data[lower_index]
            upper = sorted_data[upper_index]

            percentile_value = lower + (upper - lower) * (percentile - lower_index / (len(data) - 1)) * (len(data) - 1)
            result.append(percentile_value)

        return result


if __name__ == "__main__":
    mock_generator = FibonacciDistributionGenerator(10)
    mock_generator.getElements = types.MethodType(lambda s: [1, 10, 50], mock_generator)

    generators = [mock_generator, StepByStepDistributionGenerator(1, 100, 1), NormalDistributionGenerator(0, 10, 100),
                  FibonacciDistributionGenerator(20)]
    percentile_calculators = [NearestRankPercentileCalculator(), LinearInterpolationPercentileCalculator()]
    number_of_percentiles = 10

    for g in generators:
        for p in percentile_calculators:
            tester = DistributionTester(g, p)
            tester.test(number_of_percentiles)
