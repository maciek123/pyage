import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype

class AbstractCrossover(Operator):
    def __init__(self, type, size):
        super(AbstractCrossover, self).__init__(type)
        self.size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)


class AverageCrossover(AbstractCrossover):
    def __init__(self, type=None, size=100):
        super(AverageCrossover, self).__init__(type, size)
        self.size = size

    def cross(self, p1, p2):
        genotype = PointGenotype((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)
        return genotype



