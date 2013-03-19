import pprint
import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype

class PointMutation(Operator):
    def __init__(self):
        super(PointMutation, self).__init__(PointGenotype)

    def process(self, population):
        max_fitness = max(genotype.fitness for genotype in population)
        for genotype in population:
            range = abs(max_fitness - genotype.fitness) + 0.001
            genotype.x = genotype.x + random.uniform(-range, range)
