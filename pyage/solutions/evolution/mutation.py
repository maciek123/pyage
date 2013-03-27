import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype

class AbstractMutation:
    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.mutate(genotype)


class UniformPointMutation(Operator, AbstractMutation):
    def __init__(self, probability=0.1, radius=100.5):
        super(UniformPointMutation, self).__init__(PointGenotype)
        self.probability = probability
        self.radius = radius


    def mutate(self, genotype):
        genotype.x = genotype.x + random.uniform(-self.radius, self.radius)
        genotype.y = genotype.y + random.uniform(-self.radius, self.radius)


