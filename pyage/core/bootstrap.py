import threading
import Pyro4
import sys
from pyage.core import inject
from pyage.core.workspace import Workspace

if __name__ == '__main__':
    inject.config = sys.argv[1]
    workspace = Workspace()
    workspace.publish()
    workspace.publish_agents()
    print workspace.address
    threading.Thread(target=workspace.daemon.requestLoop).start()
    while True:
        workspace.step()

