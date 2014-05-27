import logging
import time
from pyage.core.statistics import Statistics

logger = logging.getLogger(__name__)


class StepStatistics(Statistics):
    def __init__(self, output_file_name='fitness_pyage.txt'):
        self.history = []
        self.fitness_output = open(output_file_name, 'a')

    def __del__(self):
        self.fitness_output.close()

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(step_count - 1) + ';' + str(abs(best_fitness)) + '\n')

    def update(self, step_count, agents):
        try:
            best_fitness = max(a.get_fitness() for a in agents)
            logger.info(best_fitness)
            self.history.append(best_fitness)
            if (step_count - 1) % 100 == 0:
                self.append(best_fitness, step_count)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness()).get_best_genotype())
        except:
            logging.exception("")


class TimeStatistics(StepStatistics):
    def __init__(self, output_file_name='fitness_pyage.txt'):
        super(TimeStatistics, self).__init__(output_file_name)
        self.start = time.time()

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(time.time() - self.start) + ';' + str(best_fitness) + '\n')
