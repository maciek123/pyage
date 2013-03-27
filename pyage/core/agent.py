import logging
import random
from pyage.core.address import Addressable
from pyage.core.inject import Inject


logger = logging.getLogger(__name__)

AGENT = "agent"

class AbstractAgent:
    def initialize(self):
        self.initializer.process(self.population)

    def get_address(self):
        return self.address

    def get_fitness(self):
        return max(genotype.fitness for genotype in self.population)

    def add_genotype(self, population):
        logger.debug("received genotype!")
        self.population.extend(population)

    @Inject("operators", "initializer")
    def validate_operators(self):
        for o in self.operators:
            if not o.is_compatible(self.initializer):
                raise ValueError("operator %s is not compatible with %s" % (o, self.initializer))


class Agent(Addressable, AbstractAgent):
    @Inject("locator", "migration")
    def __init__(self, name=None):
        self.name = name
        super(Agent, self).__init__()
        logger.debug("address:" + self.address)
        self.population = []
        self.validate_operators()
        self.initialize()
        self.steps = 0

    def step(self):
        self.steps += 1
        logger.debug("%s %s %s",self.steps, self.address, self.get_fitness())
        for o in self.operators:
            o.process(self.population)
        self.__send_genotype()
        self.__migrate()

    def __send_genotype(self):
        if random.random() < 0.01:
            try:
                neighbour = self.locator.get_neighbour(self)
                if neighbour:
                    logger.debug("neighbour: %s", neighbour.get_address())
                    probe = list(self.population.sort(key=lambda g:g.fitness))[:20:2]
                    neighbour.add_genotype(probe)
            except:
                logging.exception('')

    def __migrate(self):
        self.migration.migrate(self)


class AggregateAgent(Addressable, AbstractAgent):
    @Inject("aggregated_agents:_AggregateAgent__agents")
    def __init__(self, name=None):
        self.name = name
        super(AggregateAgent, self).__init__()
        for agent in self.__agents.values():
            agent.parent = self
        self.steps = 0

    def step(self):
        for agent in self.__agents.values():
            agent.step()

    def remove_agent(self, agent):
        agent = self.__agents[agent.get_address()]
        del self.__agents[agent.get_address()]
        agent.parent = None
        return agent

    def add_agent(self, agent):
        agent.parent = self
        self.__agents[agent.get_address()] = agent

    def get_agents(self):
        return self.__agents.values()

    def get_fitness(self):
        return max(agent.get_fitness() for agent in self.__agents.values())


def agents_factory(*args):
    def factory():
        agents = {}
        for name in args:
            agent = Agent(name)
            agents[agent.get_address()] = agent
        return agents

    return factory


def aggregate_agents_factory(*args):
    def factory():
        agents = {}
        for name in args:
            agent = AggregateAgent(name)
            agents[agent.get_address()] = agent
        return agents

    return factory
