from pyage.inject import Inject

class Computation:
    @Inject("population_generator", "stop_condition", "op")
    def __init__(self):
        pass

    def run(self):
        population = self.population_generator()
        print population
        while True:
            for operator in self.op:
                operator(population)
            if  self.stop_condition.should_stop(population):
                break
