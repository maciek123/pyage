import logging
import matplotlib
import pylab

logger = logging.getLogger(__name__)

class SimpleStatistics(object):
    def __init__(self):
        self.history = []

    def update(self, step_count, agents):
        try:
            self.history.append(max(a.get_fitness() for a in agents))
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a:a.get_fitness).get_best_genotype())
            pylab.plot(self.history[99:])
            pylab.savefig('plot.png')
        except:
            logging.exception("")
