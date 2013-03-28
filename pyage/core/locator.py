import logging
import random
import Pyro4
from pyage.core.agent import AGENT
from pyage.core.inject import Inject

logger = logging.getLogger(__name__)


class Pyro4Locator(object):
    @Inject("ns_hostname")
    def __init__(self):
        super(Pyro4Locator, self).__init__()

    def get_neighbour(self, agent):
        try:
            random_agent = self.__get_random_agent(agent)
            logger.debug(random_agent.get_address())
            return  random_agent
        except:
            logging.exception('')

    def __get_random_agent(self, a):
        ns = Pyro4.locateNS(self.ns_hostname)
        agents = ns.list(AGENT)
        logger.debug(agents)
        del agents[AGENT + "." + a.address]
        return Pyro4.Proxy(random.choice(agents.values()))


class ParentLocator(object):
    def get_neighbour(self, agent):
        siblings = list(agent.parent.get_agents())
        siblings.remove(agent)
        return random.choice(siblings)