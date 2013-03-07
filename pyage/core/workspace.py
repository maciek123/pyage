from pyage.core.address import Addressable

class Workspace(Addressable):
    def __init__(self, name=None):
        self.name = name
        super(Workspace, self).__init__()

        self.__agents = {}

    def get_agents(self):
        return self.__agents.values()

    def ping(self):
        return "pong"

    def step(self):
        for agent in self.__agents.values():
            agent.step()

    def add_agent(self, agent):
        self.__agents[agent.address] = agent

    def get_agent(self, address):
        return self.__agents[address]

    def remove_agent(self, address):
        agent = self.__agents[address]
        del self.__agents[address]
        return agent

