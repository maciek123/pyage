from pyage.inject import Inject

class Computation:
    @Inject("population_generator", "stop_condition", "op", "addressProvider")
    def __init__(self, config):
        pass

    def run(self):
        population = self.population_generator()
        print self.addressProvider.generateAddress(self)
        print population
        while True:
            for operator in self.op:
                operator(population)
            if  self.stop_condition.should_stop(population):
                break
