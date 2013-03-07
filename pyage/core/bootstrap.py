import threading
import Pyro4
import sys
from pyage.core import inject
from pyage.core.workspace import Workspace

if __name__ == '__main__':
    inject.config = sys.argv[1]
    import pyage_conf as pyage_conf

    workspace = Workspace(pyage_conf.workspace_name)
    for agent in pyage_conf.agents:
        workspace.add_agent(agent)
    print workspace.address
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    threading.Thread(target=daemon.requestLoop).start()
    uri = daemon.register(workspace)
    ns.register(workspace.address, uri)
    print     ns.list()
    print uri
    while True:
        workspace.step()

