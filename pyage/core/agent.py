import random
from time import sleep
from pyage.core.address import Addressable
from pyage.core.inject import Inject

class Agent(Addressable):
    @Inject("operators")
    def __init__(self, name=None):
        self.name = name
        super(Agent, self).__init__()
        print "address:", self.address
        self.fitness = 0

    def step(self):
        print "step ",
        self.fitness = random.random()
        print self.address, self.fitness
        sleep(1)

    def get_address(self):
        return self.address


def agents_factory(*args):
    return lambda: dict(map(lambda name: (name, Agent(name)), args))