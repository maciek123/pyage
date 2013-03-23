import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype

class UniformPointMutation(Operator):
    def __init__(self, probability=0.1, radius=100.5):
        super(UniformPointMutation, self).__init__(PointGenotype)
        self.probability = probability
        self.radius = radius


    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                genotype.x = genotype.x + random.uniform(-self.radius, self.radius)
