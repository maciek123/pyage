import random
from pyage.address import Addressable

class Agent(Addressable):
    def __init__(self):
        super(Agent, self).__init__()
        print self.address
        self.fitness = 0

    def step(self):
        print "step ",
        self.fitness = random.random()
        print self.fitness

    def get_address(self):
        return self.address