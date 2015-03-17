import logging
import random
from pyage.core.address import Addressable
from pyage.core.agent.agent import AbstractAgent
from pyage.core.inject import Inject, InjectOptional

logger = logging.getLogger(__name__)


class AggregateAgent(Addressable, AbstractAgent):
    @Inject("aggregated_agents:_AggregateAgent__agents")
    @InjectOptional("locator")
    def __init__(self, name=None):
        self.name = name
        super(AggregateAgent, self).__init__()
        for agent in self.__agents.values():
            agent.parent = self
        self.steps = 0

    def step(self):
        for agent in self.__agents.values():
            agent.step()
        self.steps += 1

    def remove_agent(self, agent):
        del self.__agents[agent.get_address()]
        self.locator.remove_agent(agent)
        agent.parent = None
        return agent

    def add_agent(self, agent):
        agent.parent = self
        self.__agents[agent.get_address()] = agent

    def get_agents(self):
        return self.__agents.values()

    def get_fitness(self):
        try:
            return max(agent.get_fitness() for agent in self.__agents.values())
        except ValueError:
            return None

    def get_best_genotype(self):
        return max(self.__agents.values(), key=lambda a: a.get_fitness()).get_best_genotype()

    def move(self, agent):
        allowed_moves = self.locator.get_allowed_moves(agent)
        if allowed_moves:
            self.locator.remove_agent(agent)
            destination = get_random_move(allowed_moves)
            self.locator.add_agent(agent, destination)
            logger.debug("%s moved to %s" % (agent, destination))

    def get_neighbour(self, agent):
        return self.locator.get_neighbour(agent)


def aggregate_agents_factory(*args):
    def factory():
        agents = {}
        for name in args:
            agent = AggregateAgent(name)
            agents[agent.get_address()] = agent
        return agents

    return factory


def get_random_move(allowed_moves):
    destination = random.sample(allowed_moves, 1)[0]
    return destination