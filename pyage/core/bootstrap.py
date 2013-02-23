import threading
from time import sleep
import Pyro4
from pyage.core.agent import Agent
from pyage.core.workspace import Workspace

if __name__ == '__main__':
    workspace = Workspace("workspace")
    workspace.__agents.append(Agent())
    print workspace.address
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    threading.Thread(target=daemon.requestLoop).start()
    uri = daemon.register(workspace)
    ns.register(workspace.address, uri)
    print uri
    while(True):
#        daemon.events(daemon.sockets)
        workspace.step()
        sleep(1)
