import logging
import random
import Pyro4
from pyage.core.agent import AGENT
from pyage.core.inject import Inject

class Pyro4Migration(object):

    @Inject("ns_hostname")
    def __init__(self):
        super(Pyro4Migration, self).__init__()

    def migrate(self, agent):
        try:
            if random.random() > 0.95:
                print "migrating!"
                aggregate = self.__get_random_aggregate(agent)
                print aggregate.get_address()
                aggregate.add_agent(agent.parent.remove_agent(agent))
        except:
            logging.exception("")

    def __get_random_aggregate(self,agent):
        ns = Pyro4.locateNS(self.ns_hostname)
        agents = ns.list(AGENT)
        print agents
        del agents[AGENT + "." + agent.parent.address]
        return Pyro4.Proxy(random.choice(agents.values()))


class NoMigration(object):
    def migrate(self, agent):
        pass