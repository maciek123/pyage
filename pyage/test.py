import sys
import Pyro4
import Pyro4.util

sys.excepthook = Pyro4.util.excepthook

def print_property(workspace_name, property):
    print workspace_name
    workspace = Pyro4.Proxy(workspace_name)
    print workspace.ping()
    for agent in workspace.get_agents():
        print getattr(agent, property)

print_property("PYRONAME:workspace", "fitness")
print "!"
