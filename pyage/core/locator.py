import Pyro4

def list_workspaces():
    ns = Pyro4.locateNS()
    return ns.list("workspace")

print list_workspaces()