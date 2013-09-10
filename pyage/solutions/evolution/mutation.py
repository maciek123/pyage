import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype

class AbstractMutation(Operator):
    def __init__(self, type, probability):
        super(AbstractMutation, self).__init__()
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.mutate(genotype)


class UniformPointMutation(AbstractMutation):
    def __init__(self, probability=0.1, radius=100.5):
        super(UniformPointMutation, self).__init__(PointGenotype, probability)
        self.radius = radius


    def mutate(self, genotype):
        genotype.x = genotype.x + random.uniform(-self.radius, self.radius)
        genotype.y = genotype.y + random.uniform(-self.radius, self.radius)


class UniformFloatMutation(AbstractMutation):
    def __init__(self, probability=0.1, radius=0.5):
        super(UniformFloatMutation, self).__init__(FloatGenotype, probability)
        self.radius = radius


    def mutate(self, genotype):
        index = random.randint(0, len(genotype.genes) - 1)
        genotype.genes[index] += random.uniform(-self.radius, self.radius)

