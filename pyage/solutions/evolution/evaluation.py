from math import cos, pi
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype

A = 20

class RastriginEvaluation(Operator):
    def __init__(self, type=None):
        super(RastriginEvaluation, self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__rastrigin(genotype.x, genotype.y)

    def __rastrigin(self, x, y):
        return 2 * A + x ** 2 - A * cos(2 * pi * x) + y ** 2 - A * cos(2 * pi * y)


class DeJongEvaluation(Operator):
    def __init__(self, type=None):
        super(DeJongEvaluation, self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__DeJong(genotype.x, genotype.y)

    def __DeJong(self, x, y):
        return x ** 2 + y ** 2
