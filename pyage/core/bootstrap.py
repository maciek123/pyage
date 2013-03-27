from datetime import datetime
import logging
import threading
from time import sleep
import Pyro4
import sys
from pyage.core import inject
from pyage.core.workspace import Workspace

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(filename='pyage-' + str(datetime.now()) + '.log', level=logging.DEBUG)
    inject.config = sys.argv[1]
    logging.debug("config: %s", inject.config)
    workspace = Workspace()
    workspace.publish()
    workspace.publish_agents()
    logger.debug(workspace.address)
    thread = threading.Thread(target=workspace.daemon.requestLoop)
    thread.setDaemon(True)
    thread.start()
    Pyro4.config.COMMTIMEOUT = 1
    while not workspace.stopped:
        workspace.step()
        try:
            sleep(float(sys.argv[2]))
        except IndexError:
            pass
    workspace.daemon.close()

