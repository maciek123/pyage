from math import cos, pi, sin, sqrt
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype

A = 10

class FloatRastriginEvaluation(Operator):
    def __init__(self):
        super(FloatRastriginEvaluation, self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__rastrigin(genotype.genes)

    def __rastrigin(self, genes):
        sum = len(genes) * A
        for gene in genes:
            sum += gene ** 2 - A * cos(2 * pi * gene)
        return sum


class RastriginEvaluation(Operator):
    def __init__(self):
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


class SchwefelEvaluation(Operator):
    def __init__(self):
        super(SchwefelEvaluation, self).__init__()

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__schwefel(genotype.genes)

    def __schwefel(self, genes):
        sum = 418.9829
        for gene in genes:
            sum += -gene * sin(sqrt(abs(gene)))
        return sum

