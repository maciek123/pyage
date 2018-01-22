import logging
import random
from pyage.core.operator import Operator
from pyage.elect.el_genotype import Votes

logger = logging.getLogger(__name__)

class AbstractMutation(Operator):
    def __init__(self, type, probability):
        super(AbstractMutation, self).__init__()
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.mutate(genotype)

class Mutation(AbstractMutation):
    def __init__(self, probability, evol_probability):
        super(Mutation, self).__init__(Votes, evol_probability)
        self.probability = probability

    def mutate(self, genotype):
        logger.debug("Mutating genotype: {0}".format(genotype))
        for vote in genotype.votes:
            rand = random.random()
            index_of_cand = vote.index(genotype.candidate)
            if rand < self.probability:
                bias = random.randint(-10,10)
                biased = (index_of_cand-bias)%len(vote)
                vote.insert(biased, vote.pop(index_of_cand))
#                vote[index_of_cand], vote[biased] = vote[biased], vote[index_of_cand]
        #logger.debug("Genotype is now: {0}".format(genotype))

				
		


