from pyage.address import Addressable

class Workspace(Addressable):
    def __init__(self, name=None):
        super(Workspace, self).__init__()
        if name:
            self.address = name
        self.__agents = {}

    def get_agents(self):
        return self.__agents.values()

    def ping(self):
        return "pong"

    def step(self):
        for agent in self.__agents:
            agent.step()

    def add_agent(self, agent):
        self.__agents[agent.address] = agent

    def get_agent(self, address):
        return self.__agents[address]

