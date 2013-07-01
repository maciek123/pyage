import logging
from Pyro4 import locateNS
from pyage.core.address import Addressable
from inject import Inject
from pyage.core.agent import AGENT

logger = logging.getLogger(__name__)

WORKSPACE = "workspace"

class Workspace(Addressable):
    @Inject("agents:_Workspace__agents", "migration", "ns_hostname", "daemon", "step_limit", "stats")
    def __init__(self):
        super(Workspace, self).__init__()
        self.steps = 0
        self.stopped = False

    def get_agents(self):
        return self.__agents.values()

    def ping(self):
        return "pong"

    def step(self):
        self.steps += 1
        logger.info("=========STEP %s=============", self.steps)
        for agent in self.__agents.values():
            agent.step()
        self.stats.update(self.steps, self.__agents.values())
        if self.steps > self.step_limit:
            self.stopped = True
            self.stats.summarize(self.__agents.values())

    def publish_agents(self):
        for agent in self.__agents.values():
            try:
                uri = self.daemon.register(agent)
                ns = locateNS(self.ns_hostname)
                ns.register('%s.%s' % (AGENT, agent.address), uri)
                logger.debug(ns.list())
            except:
                logger.debug("could not locate nameserver")

    def unregister_agents(self):
        try:
            ns = locateNS(self.ns_hostname)
            for agent in self.__agents.values():
                ns.remove('%s.%s' % (AGENT, agent.address))
            logger.debug(ns.list())
        except:
            logger.debug("could not locate nameserver")

    def get_agent(self, address):
        return self.__agents[address]

    def remove_agent(self, address):
        agent = self.__agents[address]
        del self.__agents[address]
        agent.workspace = None
        return agent

    def publish(self):
        uri = self.daemon.register(self)
        try:
            ns = locateNS(self.ns_hostname)
            ns.register(WORKSPACE + '.' + self.address, uri)
            logger.debug(ns.list())
        except:
            logger.debug("could not locate nameserver")

    def unregister(self):
        try:
            ns = locateNS(self.ns_hostname)
            ns.remove(WORKSPACE + '.' + self.address)
            logger.debug(ns.list())
        except:
            logger.debug("could not locate nameserver")
