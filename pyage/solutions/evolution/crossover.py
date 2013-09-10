import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype

class AbstractCrossover(Operator):
    def __init__(self, type, size):
        super(AbstractCrossover, self).__init__(type)
        self.__size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.__size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)


class AverageCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(AverageCrossover, self).__init__(PointGenotype, size)

    def cross(self, p1, p2):
        genotype = PointGenotype((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)
        return genotype


class AverageFloatCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(AverageFloatCrossover, self).__init__(FloatGenotype, size)

    def cross(self, p1, p2):
        genotype = FloatGenotype([sum(p) / 2.0 for p in zip(p1.genes, p2.genes)])
        return genotype

class SinglePointCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(SinglePointCrossover, self).__init__(FloatGenotype, size)


    def cross(self, p1, p2):
        crossingPoint = random.randint(1, len(p1.genes))
        return FloatGenotype(p1.genes[:crossingPoint] + p2.genes[crossingPoint:])