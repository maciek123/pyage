import logging
import os
import urllib2
import time
import sys
from pyage.core.inject import InjectOptional, Inject

logger = logging.getLogger(__name__)


class Statistics(object):
    def update(self, step_count, agents):
        raise NotImplementedError()

    def summarize(self, agents):
        raise NotImplementedError()


class SimpleStatistics(Statistics):
    def __init__(self, plot_file_name='plot.png'):
        self.history = []
        self.plot_file_name = plot_file_name

    def update(self, step_count, agents):
        try:
            best_fitness = max(a.get_fitness() for a in agents)
            logger.info(best_fitness)
            self.history.append(best_fitness)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            import pylab
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness()).get_best_genotype())
            pylab.yscale('symlog')
            pylab.savefig(self.plot_file_name)
        except:
            logging.exception("")


class TimeStatistics(SimpleStatistics):
    @InjectOptional("notification_url")
    def __init__(self, plot_file_name='plot.png'):
        super(TimeStatistics, self).__init__(plot_file_name)
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
            import pylab
            pylab.plot(self.times, self.history)
            pylab.xlabel("time (s)")
            pylab.ylabel("fitness")
            pylab.yscale('symlog')
            pylab.savefig(self.plot_file_name)

            if hasattr(self, "notification_url"):
                url = self.notification_url + "?time=%s&agents=%s&conf=%s" % (
                    time.time() - self.start, os.environ['AGENTS'], sys.argv[1])
                logger.info(url)
                urllib2.urlopen(url)
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness()).get_best_genotype())
        except:
            logging.exception("")


class NotificationStatistics(SimpleStatistics):
    @Inject("notification_url")
    def __init__(self):
        super(NotificationStatistics, self).__init__()
        self.start = time.time()

    def summarize(self, agents):
        try:
            url = self.notification_url + "?time=%s&agents=%s&conf=%s" % (
                time.time() - self.start, os.environ['AGENTS'], sys.argv[1])
            logger.info(url)
            urllib2.urlopen(url)

        except:
            logging.exception("")


class NoStatistics(Statistics):
    def update(self, step_count, agents):
        pass

    def summarize(self, agents):
        pass

