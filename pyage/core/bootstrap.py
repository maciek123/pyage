from datetime import datetime
import logging
import os
import threading
from time import sleep, time
import urllib2
import Pyro4
import sys
from pyage.core import inject
from pyage.core.workspace import Workspace

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    start_time = time()
    logging.basicConfig(filename='pyage-' + str(datetime.now()) + '.log', level=logging.INFO)
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
    try:
        time = time() - start_time
        logger.debug("elapsed time: %s seconds", time)
        url = "http://student.agh.edu.pl/~kmaciej/pyage.php?time=%s&agents=%s&conf=%s" % (
        time, os.environ['AGENTS'], sys.argv[1])
        logger.debug(url)
        urllib2.urlopen(url)
    except:
        logger.exception("could not open url")
    workspace.daemon.close()
    workspace.unregister_agents()
    workspace.unregister()

