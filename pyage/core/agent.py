from time import sleep
from pyage.core.address import Addressable
from pyage.core.inject import Inject

AGENT = "agent"

class Agent(Addressable):
    @Inject("locator")
    def __init__(self, name=None):
        self.name = name
        super(Agent, self).__init__()
        print "address:", self.address
        self.population = []
        self.validate_operators()
        self.initialize()
        self.steps = 0

    @Inject("operators", "initializer")
    def validate_operators(self):
        for o in self.operators:
            if not o.is_compatible(self.initializer):
                raise ValueError("operator %s is not compatible with %s" % (o, self.initializer))

    def initialize(self):
        self.initializer.process(self.population)

    def step(self):
        self.steps += 1
        print self.address, self.get_fitness(), self.population
        for o in self.operators:
            o.process(self.population)
        if self.steps % 10 == 0:
            neighbour = self.locator.get_neighbour(self)
            if neighbour:
                print "neighbour: ",neighbour.get_address(), self.population
                probe = list(self.population[::2])
                neighbour.add_genotype(probe)

    def get_address(self):
        return self.address

    def get_fitness(self):
        return max(genotype.fitness for genotype in self.population)

    def add_genotype(self, population):
        print "received genotype: ", population
        self.population.extend(population)


def agents_factory(*args):
    return lambda: dict(map(lambda name: (name, Agent(name)), args))