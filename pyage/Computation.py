from pyage.Inject import Inject

class Computation:
    @Inject("population_generator", "stop_condition", "op", "addressProvider", "myEvent")
    def __init__(self):
        pass

    def run(self):
        population = self.population_generator()
        print self.addressProvider.generateAddress(self)
        print population
        while True:
            for operator in self.op:
                operator(population)
            if  self.stop_condition(population):
                break
        print population