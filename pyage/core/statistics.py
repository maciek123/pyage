import logging
import matplotlib
import pylab

logger = logging.getLogger(__name__)

class SimpleStatistics(object):
    def __init__(self):
        self.history = []

    def update(self, step_count, agents):
        self.history.append(max(a.get_fitness() for a in agents))

    def summarize(self, agents):
        logger.debug(self.history)
        logger.debug("best genotype: %s", max(agents, key=lambda a:a.get_fitness).get_best_genotype())
        pylab.plot(self.history[4:])
        pylab.savefig('plot.png')
