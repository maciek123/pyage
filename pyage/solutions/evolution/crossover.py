import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype

class AverageCrossover(Operator):
    def __init__(self, type=None, size=100):
        super(AverageCrossover, self).__init__()
        self.size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.size):
            p1, p2 = random.sample(parents, 2)
            population.append(PointGenotype((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0))

