import random
from time import sleep
from pyage.core.address import Addressable
from pyage.core.inject import Inject

class Agent(Addressable):
    def __init__(self, name=None):
        self.name = name
        super(Agent, self).__init__()
        print "address:", self.address
        self.population = []
        self.validate_operators()
        self.initialize()

    @Inject("operators", "initializer")
    def validate_operators(self):
        for o in self.operators:
            if not o.is_compatible(self.initializer):
                raise ValueError("operator %s is not compatible with %s" % (o, self.initializer))

    def initialize(self):
        self.initializer.process(self.population)

    def step(self):
        print "step ",
        print self.address, self.get_fitness(), self.operators
        for o in self.operators:
            o.process(self.population)
        sleep(1)

    def get_address(self):
        return self.address

    def get_fitness(self):
        return max(genotype.fitness for genotype in self.population)


def agents_factory(*args):
    return lambda: dict(map(lambda name: (name, Agent(name)), args))