import logging
import random
from pyage.core.address import Addressable
from pyage.core.inject import Inject


logger = logging.getLogger(__name__)

AGENT = "agent"

class AbstractAgent:
    def initialize(self):
        self.initializer.process(self.population)

    def get_fitness(self):
        return max(genotype.fitness for genotype in self.population)

    def get_best_genotype(self):
        return max(self.population, key=lambda g: g.fitness)

    def add_genotype(self, population):
        logger.debug("received genotype!")
        self.population.extend(population)

    @Inject("operators", "initializer")
    def validate_operators(self):
        for o in self.operators:
            if not o.is_compatible(self.initializer):
                raise ValueError("operator %s is not compatible with %s" % (o, self.initializer))


class Agent(Addressable, AbstractAgent):
    @Inject("locator", "migration")
    def __init__(self, name=None):
        self.name = name
        super(Agent, self).__init__()
        logger.debug("address:" + self.address)
        self.population = []
        self.validate_operators()
        self.initialize()
        self.steps = 0

    def step(self):
        self.steps += 1
        logger.debug("%s %s %s", self.steps, self.address, self.get_fitness())
        for o in self.operators:
            o.process(self.population)
        self.__send_genotype()
        self.__migrate()

    def __send_genotype(self):
        if random.random() < 0.01:
            try:
                neighbour = self.locator.get_neighbour(self)
                if neighbour:
                    logger.debug("neighbour: %s", neighbour.get_address())
                    probe = list(self.population.sort(key=lambda g: g.fitness))[:20:2]
                    neighbour.add_genotype(probe)
            except:
                logging.exception('')

    def __migrate(self):
        self.migration.migrate(self)


class EmasAgent(Addressable):
    @Inject("locator", "migration", "evaluation", "crossover", "mutation")
    def __init__(self, genotype, energy, name=None):
        self.name = name
        super(EmasAgent, self).__init__()
        self.genotype = genotype
        self.energy = energy
        self.steps = 0
        self.evaluation.process([genotype])

    def step(self):
        self.steps += 1
        logger.debug("%s %s %s %s", self.steps, self.address, self.get_fitness(), self.energy)
        try:
            neighbour = self.locator.get_neighbour(self)
            if neighbour:
                logger.debug("neighbour: %s", neighbour.get_address())
                if self.energy < 2:
                    self.death(neighbour)
                elif self.energy > 12 and neighbour.get_energy() > 12:
                    self.reproduce(neighbour)
                elif self.energy > 10:
                    self.migration.migrate(self)
                else:
                    self.meet(neighbour)
        except:
            logging.exception('')

    def get_fitness(self):
        return self.genotype.fitness

    def get_best_genotype(self):
        return self.genotype

    def add_energy(self, energy):
        self.energy += energy

    def get_energy(self):
        return self.energy

    def get_genotype(self):
        return self.genotype

    def meet(self, neighbour):
        if self.get_fitness() > neighbour.get_fitness():
            self.energy += 1
            neighbour.add_energy(-1)
        elif self.get_fitness() < neighbour.get_fitness():
            self.energy -= 1
            neighbour.add_energy(1)

    def death(self, neighbour):
        neighbour.add_energy(self.energy)
        self.energy = 0
        self.parent.remove_agent(self)

    def reproduce(self, neighbour):
        logger.debug("reproducing!")
        energy = 10
        self.energy -= 5
        neighbour.add_energy(-5)
        genotype = self.crossover.cross(self.genotype, neighbour.get_genotype())
        self.mutation.mutate(genotype)
        self.parent.add_agent(EmasAgent(genotype, energy))


class AggregateAgent(Addressable, AbstractAgent):
    @Inject("aggregated_agents:_AggregateAgent__agents")
    def __init__(self, name=None):
        self.name = name
        super(AggregateAgent, self).__init__()
        for agent in self.__agents.values():
            agent.parent = self
        self.steps = 0

    def step(self):
        for agent in self.__agents.values():
            agent.step()

    def remove_agent(self, agent):
        agent = self.__agents[agent.get_address()]
        del self.__agents[agent.get_address()]
        agent.parent = None
        return agent

    def add_agent(self, agent):
        agent.parent = self
        self.__agents[agent.get_address()] = agent

    def get_agents(self):
        return self.__agents.values()

    def get_fitness(self):
        return max(agent.get_fitness() for agent in self.__agents.values())

    def get_best_genotype(self):
        return max(self.__agents.values(), key=lambda a: a.get_fitness()).get_best_genotype()


def agents_factory(*args):
    def factory():
        agents = {}
        for name in args:
            agent = Agent(name)
            agents[agent.get_address()] = agent
        return agents

    return factory


def aggregate_agents_factory(*args):
    def factory():
        agents = {}
        for name in args:
            agent = AggregateAgent(name)
            agents[agent.get_address()] = agent
        return agents

    return factory
