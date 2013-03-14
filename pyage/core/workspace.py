from pyage.core.address import Addressable
from inject import Inject

class Workspace(Addressable):
    @Inject("workspace_name:name", "agents:_Workspace__agents")
    def __init__(self):
        super(Workspace, self).__init__()

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

