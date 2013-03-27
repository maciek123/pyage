import logging
import matplotlib
import pylab

logger = logging.getLogger(__name__)

class SimpleStatistics(object):
    def __init__(self):
        self.history = []

    def update(self, step_count, agents):
        self.history.append(max(a.get_fitness() for a in agents))

    def summarize(self):
        logger.debug(self.history)
        pylab.plot(self.history[5::2])
        pylab.savefig('plot.png')
