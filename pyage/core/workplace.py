import logging
from pyage.core.address import Addressable
from pyage.core.inject import Inject, InjectOptional
from pyage.core.agent.agent import AGENT
import signal

logger = logging.getLogger(__name__)

try:
    from Pyro4 import locateNS
except:
    print "Pyro4 not installed, running in local mode only"

WORKPLACE = "workplace"


class Workplace(Addressable):
    @Inject("agents:_Workplace__agents", "stop_condition", "stats")
    @InjectOptional("ns_hostname", "daemon")
    def __init__(self):
        super(Workplace, self).__init__()
        for agent in self.__agents.values():
            agent.parent = self
        self.steps = 0
        self.stopped = False
        self.best_known_fitness = -float("inf")

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
        try:
            for a in self.__agents.values():
                a.stop()
        except AttributeError:
            pass  # "old style" agents (pre pyage 1.1) don't have such method

    def step(self):
        try:
            self.steps += 1
            logger.info("=========STEP %s=============", self.steps)
            for agent in self.__agents.values():
                agent.step()
            self.stats.update(self.steps, self.__agents.values())
            if self.stop_condition.should_stop(self):
                self.stop()
        except:
            logger.warning("Caught exception, stopping")
            logging.exception("exception in step %s" % self.steps)
            self.stop()

    def get_fitness(self):
        return max(a.get_fitness() for a in self.get_agents())

    def get_best_known_fitness(self):
        return self.best_known_fitness

    def set_best_known_fitness(self, fitness):
        logger.info("new best fitness registered: " + str(fitness))
        self.best_known_fitness = fitness

    def get_agent(self, address):
        return self.__agents[address]

    def remove_agent(self, address):
        agent = self.__agents[address]
        del self.__agents[address]
        agent.workspace = None
        return agent

    def publish(self):
        if hasattr(self, "ns_hostname") and hasattr(self, "daemon"):
            uri = self.daemon.register(self)
            try:
                ns = locateNS(self.ns_hostname)
                ns.register(WORKPLACE + '.' + self.address, uri)
                logger.debug(ns.list())
                self.publish_agents()
            except:
                logger.debug("could not locate nameserver")

    def publish_agents(self):
        for agent in self.__agents.values():
            try:
                uri = self.daemon.register(agent)
                ns = locateNS(self.ns_hostname)
                ns.register('%s.%s' % (AGENT, agent.address), uri)
                logger.debug(ns.list())
            except:
                logger.debug("could not locate nameserver")

    def unregister(self):
        try:
            self.unregister_agents()
            ns = locateNS(self.ns_hostname)
            ns.remove(WORKPLACE + '.' + self.address)
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
