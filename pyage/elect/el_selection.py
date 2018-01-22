import random
from pyage.core.operator import Operator

class TournamentSelection(Operator):
    def __init__(self, type=None, size=20, tournament_size=20):
        super(TournamentSelection, self).__init__()
        self.size = size
        self.tournament_size = tournament_size

    def process(self, population):
        p = list(population)
        population[:] = []
        for i in range(self.size):
            sample = random.sample(p, self.tournament_size)
            winner = max(sample, key=lambda genotype: genotype.fitness)
            population.append(winner)
