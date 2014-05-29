import logging
from pyage.core.address import Addressable
from pyage.core.inject import Inject

logger = logging.getLogger(__name__)


class EmasAgent(Addressable):
    @Inject("locator", "migration", "evaluation", "crossover", "mutation", "emas", "transferred_energy")
    def __init__(self, genotype, energy, name=None):
        self.name = name
        super(EmasAgent, self).__init__()
        self.genotype = genotype
        self.energy = energy
        self.steps = 0
        self.evaluation.process([genotype])

    def step(self):
        self.steps += 1
        try:
            neighbour = self.locator.get_neighbour(self)
            if neighbour:
                if self.emas.should_die(self):
                    self.death(neighbour)
                elif self.emas.should_reproduce(self, neighbour):
                    self.emas.reproduce(self, neighbour)
                else:
                    self.meet(neighbour)
                if self.emas.can_migrate(self):
                    self.migration.migrate(self)
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
        logger.debug(str(self) + "meets" + str(neighbour))
        if self.get_fitness() > neighbour.get_fitness():
            transfered_energy = min(self.transferred_energy, neighbour.energy)
            self.energy += transfered_energy
            neighbour.add_energy(-transfered_energy)
        elif self.get_fitness() < neighbour.get_fitness():
            transfered_energy = min(self.transferred_energy, self.energy)
            self.energy -= transfered_energy
            neighbour.add_energy(transfered_energy)

    def death(self, neighbour):
        self.distribute_energy()
        self.energy = 0
        self.parent.remove_agent(self)
        logger.debug(str(self) + "died!")

    def distribute_energy(self):
        logger.debug("death, energy level: %d" % self.energy)
        if self.energy > 0:
            siblings = set(self.parent.get_agents())
            siblings.remove(self)
            portion = self.energy / len(siblings)
            if portion > 0:
                logger.debug("passing %d portion of energy to %d agents" % (portion, len(siblings)))
                for agent in siblings:
                    agent.add_energy(portion)
            left = self.energy % len(siblings)
            logger.debug("distributing %d left energy" % left)
            while left > 0:
                e = min(left, 1)
                siblings.pop().add_energy(e)
                left -= e


class EmasService(object):
    @Inject("minimal_energy", "reproduction_minimum", "migration_minimum", "newborn_energy")
    def __init__(self):
        super(EmasService, self).__init__()

    def should_die(self, agent):
        return agent.get_energy() <= self.minimal_energy

    def should_reproduce(self, a1, a2):
        return a1.get_energy() > self.reproduction_minimum and a2.get_energy() > self.reproduction_minimum

    def can_migrate(self, agent):
        return agent.get_energy() > self.migration_minimum and len(agent.parent.get_agents()) > 10

    def reproduce(self, a1, a2):
        logger.debug(str(a1) + " " + str(a2) + "reproducing!")
        energy = self.newborn_energy / 2 * 2
        a1.energy -= self.newborn_energy / 2
        a2.add_energy(-self.newborn_energy / 2)
        genotype = a1.crossover.cross(a1.genotype, a2.get_genotype())
        a1.mutation.mutate(genotype)
        a1.parent.add_agent(EmasAgent(genotype, energy))

