import sys
import Pyro4
import Pyro4.util
from pyage.core.agent import Agent

from pyage.core.query import query_property
from pyage.core.migration import migrate_agent

sys.excepthook = Pyro4.util.excepthook

def print_property(workspace_name, property):
    print workspace_name
    workspace = Pyro4.Proxy(workspace_name)
    print workspace.ping()
    workspace.add_agent(Agent())
    for agent in workspace.get_agents():
        print getattr(agent, property)

print query_property("workspace@Max:3945", "2247261", "fitness")
migrate_agent("workspace@Max:3945", "workspace", "2247261")
print "!"
