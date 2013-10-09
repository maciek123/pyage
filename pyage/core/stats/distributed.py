import logging
import Pyro4
from pyage.core.inject import Inject
from pyage.core.statistics import Statistics
from pyage.core.workplace import WORKPLACE

logger = logging.getLogger(__name__)

class GlobalStepStatistics(Statistics):
    @Inject("ns_hostname")
    def __init__(self):
        super(GlobalStepStatistics, self).__init__()
        self.fitness_output = open('fitness_pyage.txt', 'a')

    def update(self, step_count, agents):
        if step_count % 100 == 0:
            ns = Pyro4.locateNS(self.ns_hostname)
            best_fitness = max(Pyro4.Proxy(w).get_fitness() for w in ns.list(WORKPLACE).values())
            self.append(best_fitness, step_count)


    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(step_count) + ';' + str(abs(best_fitness)) + '\n')

    def summarize(self, agents):
        pass