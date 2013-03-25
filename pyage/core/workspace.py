import Pyro4
from pyage.core.address import Addressable
from inject import Inject
from pyage.core.agent import AGENT

WORKSPACE = "workspace"

class Workspace(Addressable):
    @Inject("agents:_Workspace__agents", "migration", "ns_hostname", "daemon", "step_limit")
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
        for agent in self.__agents.values():
            agent.step()
        if self.steps > self.step_limit:
            self.stopped = True

    def publish_agents(self):
        for agent in self.__agents.values():
            try:
                uri = self.daemon.register(agent)
                ns = Pyro4.locateNS(self.ns_hostname)
                ns.register('%s.%s' % (AGENT, agent.address), uri)
                print( ns.list())
            except:
                print "could not locate nameserver"

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
            ns = Pyro4.locateNS(self.ns_hostname)
            ns.register(WORKSPACE + '.' + self.address, uri)
            print( ns.list())
        except:
            print "could not locate nameserver"
