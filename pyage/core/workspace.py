from pyage.core.address import Addressable
from inject import Inject

class Workspace(Addressable):
    @Inject("workspace_name:name", "agents:_Workspace__agents", "migration")
    def __init__(self):
        super(Workspace, self).__init__()
        self.steps = 0

    def get_agents(self):
        return self.__agents.values()

    def ping(self):
        return "pong"

    def step(self):
        self.steps += 1
        for agent in self.__agents.values():
            agent.step()

    def add_agent(self, agent):
        self.__agents[agent.address] = agent
        agent.workspace = self

    def get_agent(self, address):
        return self.__agents[address]

    def remove_agent(self, address):
        agent = self.__agents[address]
        del self.__agents[address]
        agent.workspace = None
        return agent

