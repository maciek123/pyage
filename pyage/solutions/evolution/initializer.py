import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype

class PointInitializer(Operator):
    def __init__(self, size=100, lowerbound = 0.0, upperbound = 1.0):
        super(PointInitializer, self).__init__(PointGenotype)
        self.size = size
        self.lowerbound = lowerbound
        self.upperbound = upperbound

    def process(self, population):
        for i in range(self.size):
            population.append(PointGenotype(self.__randomize(), self.__randomize()))

    def __randomize(self):
        return random.uniform(self.lowerbound, self.upperbound)

