import logging
from Pyro4 import locateNS
from pyage.core.address import Addressable
from inject import Inject
from pyage.core.agent.agent import AGENT
import signal

logger = logging.getLogger(__name__)

WORKSPACE = "workplace"

class Workplace(Addressable):
    @Inject("agents:_Workplace__agents", "migration", "ns_hostname", "daemon", "stop_condition", "stats")
    def __init__(self):
        super(Workplace, self).__init__()
        self.steps = 0
        self.stopped = False
        def signal_handler(signal, frame):
            print 'You pressed Ctrl+C!'
            self.stop()
        signal.signal(signal.SIGINT, signal_handler)

    def get_agents(self):
        return self.__agents.values()

    def ping(self):
        return "pong"

    def stop(self):
        self.stopped = True
        self.stats.summarize(self.__agents.values())

    def step(self):
        self.steps += 1
        logger.info("=========STEP %s=============", self.steps)
        for agent in self.__agents.values():
            agent.step()
        self.stats.update(self.steps, self.__agents.values())
        if self.stop_condition.should_stop(self):
            self.stop()

    def get_fitness(self):
        return max(a.get_fitness() for a in self.get_agents())


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
