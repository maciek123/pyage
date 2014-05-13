import logging
from math import sqrt, ceil
import random
import Pyro4
from pyage.core.agent.agent import AGENT
from pyage.core.inject import Inject

logger = logging.getLogger(__name__)


class Locator(object):
    def get_neighbour(self, agent):
        raise NotImplementedError()


class Pyro4Locator(Locator):
    @Inject("ns_hostname")
    def __init__(self):
        super(Pyro4Locator, self).__init__()

    def get_neighbour(self, agent):
        try:
            random_agent = self.__get_random_agent(agent)
            logger.debug(random_agent.get_address())
            return random_agent
        except:
            logging.exception('')

    def __get_random_agent(self, a):
        ns = Pyro4.locateNS(self.ns_hostname)
        agents = ns.list(AGENT)
        logger.debug(agents)
        del agents[AGENT + "." + a.address]
        return Pyro4.Proxy(random.choice(agents.values()))


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