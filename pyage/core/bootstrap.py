import threading
import Pyro4
import sys
from pyage.core import inject
from pyage.core.workspace import Workspace

if __name__ == '__main__':
    inject.config = sys.argv[1]
    workspace = Workspace()
    print workspace.address
    daemon = Pyro4.Daemon()
    uri = daemon.register(workspace)
    try:
        ns = Pyro4.locateNS(sys.argv[2])
        ns.register(workspace.address, uri)
        print( ns.list())
    except:
        print "could not locate nameserver"
    threading.Thread(target=daemon.requestLoop).start()
    print uri
    while True:
        workspace.step()

