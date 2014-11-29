import logging
from math import sqrt, ceil
import random

logger = logging.getLogger(__name__)


class Locator(object):
    def get_neighbour(self, agent):
        raise NotImplementedError()


class RandomLocator(Locator):
    def get_neighbour(self, agent):
        siblings = list(agent.parent.get_agents())
        if len(siblings) < 2:
            return None
        siblings.remove(agent)
        return random.choice(siblings)


class RowLocator(Locator):
    def get_neighbour(self, agent):
        siblings = list(agent.parent.get_agents())
        if len(siblings) < 2:
            return None
        index = siblings.index(agent)
        return random.choice(siblings[index - 2:index] + siblings[index + 1:index + 3])


class GridLocator(Locator):
    def get_neighbour(self, agent):
        siblings = list(agent.parent.get_agents())
        if len(siblings) < 2:
            return None
        index = siblings.index(agent)
        size = len(siblings)
        dim = int(ceil(sqrt(size)))
        return siblings[random.choice([index - dim, index - 1, index + 1, index + dim]) % size]