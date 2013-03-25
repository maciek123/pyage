import logging
import random
import Pyro4
from pyage.core.agent import AGENT
from pyage.core.inject import Inject

class Pyro4Locator(object):
    @Inject("ns_hostname")
    def __init__(self):
        super(Pyro4Locator, self).__init__()

    def list_workspaces(self):
        ns = Pyro4.locateNS()
        return ns.list("workspace")

    def get_neighbour(self, agent):
        try:
            random_agent = self.__get_random_agent(agent)
            print random_agent.get_address()
            return  random_agent
        except:
            logging.exception('')

    def __get_random_agent(self, a):
        ns = Pyro4.locateNS(self.ns_hostname)
        agents = ns.list(AGENT)
        print agents
        del agents[AGENT + "." + a.address]
        return Pyro4.Proxy(random.choice(agents.values()))

