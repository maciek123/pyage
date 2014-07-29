from datetime import datetime
import logging
import threading
from time import time
import sys

from pyage.core import inject

from pyage.core.workplace import Workplace


logger = logging.getLogger(__name__)

if __name__ == '__main__':
    start_time = time()
    level = logging.INFO
    if len(sys.argv) >= 3:
        level = getattr(logging, sys.argv[2].upper(), None)
    logging.basicConfig(filename='pyage-' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.log', level=level)
    inject.config = sys.argv[1]
    logging.debug("config: %s", inject.config)
    workplace = Workplace()
    workplace.publish()
    logger.debug(workplace.address)
    if hasattr(workplace, "daemon"):
        thread = threading.Thread(target=workplace.daemon.requestLoop)
        thread.setDaemon(True)
        thread.start()
        import Pyro4
        Pyro4.config.COMMTIMEOUT = 1
    while not workplace.stopped:
        workplace.step()
    time = time() - start_time
    logger.debug("elapsed time: %s seconds", time)
    if hasattr(workplace, "daemon"):
        workplace.daemon.close()
    workplace.unregister()