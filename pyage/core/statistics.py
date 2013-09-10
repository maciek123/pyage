import logging
import os
import urllib2
import pylab
import time
import sys
from pyage.core.inject import InjectOptional

logger = logging.getLogger(__name__)

class Statistics(object):
    def update(self, step_count, agents):
        raise NotImplementedError()

    def summarize(self, agents):
        raise NotImplementedError()


class SimpleStatistics(Statistics):
    def __init__(self):
        self.history = []

    def update(self, step_count, agents):
        try:
            best_fitness = max(a.get_fitness() for a in agents)
            logger.info(best_fitness)
            self.history.append(best_fitness)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness).get_best_genotype())
            pylab.yscale('symlog')
            pylab.savefig('plot.png')
        except:
            logging.exception("")


class TimeStatistics(SimpleStatistics):
    @InjectOptional("notification_url")
    def __init__(self):
        super(TimeStatistics, self).__init__()
        self.times = []
        self.start = time.time()

    def update(self, step_count, agents):
        super(TimeStatistics, self).update(step_count, agents)
        try:
            self.times.append(time.time() - self.start)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            pylab.plot(self.times, self.history)
            pylab.xlabel("time (s)")
            pylab.ylabel("fitness")
            pylab.yscale('symlog')
            pylab.savefig('plot.png')

            if hasattr(self, "notification_url"):
                url = self.notification_url + "?time = % s & agents = % s & conf = % s" % (
                    time, os.environ['AGENTS'], sys.argv[1])
                logger.debug(url)
                urllib2.urlopen(url)

        except:
            logging.exception("")

