import threading
from time import sleep
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
    thread = threading.Thread(target=workspace.daemon.requestLoop)
    thread.setDaemon(True)
    thread.start()
    Pyro4.config.COMMTIMEOUT = 1
    while not workspace.stopped:
        workspace.step()
        if sys.argv[2]:
            sleep(int(sys.argv[2]))
    workspace.daemon.close()

