import random
from pyage.core.emas import EmasAgent
from pyage.core.operator import Operator
from pyage.elect.el_genotype import Votes
from pyage.core.inject import Inject
import random

class EmasInitializer(object):

    def __init__(self,votes,candidate, energy, size):
        self.votes = votes
        self.candidate = candidate
        self.energy = energy
        self.size = size

    @Inject("naming_service")
    def __call__(self):
        agents = {}
        for i in range(self.size):
            agent = EmasAgent(Votes(self.votes, self.candidate), self.energy, self.naming_service.get_next_agent())
            agents[agent.get_address()] = agent
        return agents 

    

def root_agents_factory(count, type):
    def factory():
        agents = {}
        for i in range(count):
            agent = type('R' + str(i))
            agents[agent.get_address()] = agent
        return agents

    return factory

class VotesInitializer(object):

    def __init__(self, candidates_nr, voters_nr, c_nr, seed):
        self.candidates_nr = candidates_nr
        self.voters_nr = voters_nr
        random.seed(seed)
        self.c_nr = c_nr

    def __call__(self):
        basis = range(1,self.candidates_nr+1)
        votes_list = [(random.shuffle(basis), list(basis))[1] for _ in xrange(self.voters_nr)]
        c_places_list = [vote.index(self.c_nr) for vote in votes_list]
        random.seed()
        return votes_list, c_places_list    