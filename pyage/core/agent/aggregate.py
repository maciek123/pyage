from pyage.core.address import Addressable
from pyage.core.agent.agent import AbstractAgent
from pyage.core.inject import Inject

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
        try:
            return max(agent.get_fitness() for agent in self.__agents.values())
        except ValueError:
            return None

    def get_best_genotype(self):
        return max(self.__agents.values(), key=lambda a: a.get_fitness()).get_best_genotype()


def aggregate_agents_factory(*args):
    def factory():
        agents = {}
        for name in args:
            agent = AggregateAgent(name)
            agents[agent.get_address()] = agent
        return agents

    return factory