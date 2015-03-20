import logging
import random

from pyage.core.address import Addressable
from pyage.core.agent.aggregate import get_random_move
from pyage.core.inject import Inject, InjectWithDefault


logger = logging.getLogger(__name__)


class EmasAgent(Addressable):
    @Inject("migration", "evaluation", "crossover", "mutation", "emas", "transferred_energy")
    @InjectWithDefault(("mutation_probability", 0.01))
    def __init__(self, genotype, energy, name=None):
        self.name = name
        super(EmasAgent, self).__init__()
        self.genotype = genotype
        self.energy = energy
        self.steps = 0
        self.dead = False
        self.evaluation.process([genotype])

    def step(self):
        self.steps += 1
        if self.dead:
            return
        try:
            neighbour = self.parent.get_neighbour(self)
            if neighbour:
                if self.emas.should_die(self):
                    self.death()
                elif self.emas.should_reproduce(self, neighbour):
                    self.emas.reproduce(self, neighbour)
                else:
                    self.meet(neighbour)
            if self.emas.can_migrate(self):
                self.migration.migrate(self)
            elif self.parent and self.emas.should_move(self):
                self.parent.move(self)
        except:
            logging.exception('')

    def get_fitness(self):
        return self.genotype.fitness

    def get_best_genotype(self):
        return self.genotype

    def add_energy(self, energy):
        self.energy += energy
        if self.emas.should_die(self):
            self.death()

    def get_energy(self):
        return self.energy

    def get_genotype(self):
        return self.genotype

    def meet(self, neighbour):
        logger.debug(str(self) + "meets" + str(neighbour))
        if self.get_fitness() > neighbour.get_fitness():
            transferred_energy = min(self.transferred_energy, neighbour.energy)
            self.energy += transferred_energy
            neighbour.add_energy(-transferred_energy)
        elif self.get_fitness() < neighbour.get_fitness():
            transferred_energy = min(self.transferred_energy, self.energy)
            self.energy -= transferred_energy
            neighbour.add_energy(transferred_energy)
        if self.emas.should_die(self):
            self.death()

    def death(self):
        self.distribute_energy()
        self.energy = 0
        self.dead = True
        self.parent.remove_agent(self)
        logger.debug(str(self) + "died!")

    def distribute_energy(self):
        logger.debug("%s is dying, energy level: %d" % (self, self.energy))
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

    def _mutate(self):
        if random.random() < self.mutation_probability:
            self.mutation.process([self.genotype])
            self.evaluation.process([self.genotype])

    def __repr__(self):
        return "<EmasAgent@%s>" % self.get_address()


class EmasService(object):
    @Inject("minimal_energy", "reproduction_minimum", "migration_minimum", "newborn_energy")
    @InjectWithDefault(("move_probability", 0.1))
    def __init__(self):
        super(EmasService, self).__init__()

    def should_die(self, agent):
        return agent.get_energy() <= self.minimal_energy and not agent.dead

    def should_reproduce(self, a1, a2):
        return a1.get_energy() > self.reproduction_minimum and a2.get_energy() > self.reproduction_minimum \
               and a1.parent.locator.get_allowed_moves(a1)

    def can_migrate(self, agent):
        return agent.get_energy() > self.migration_minimum and len(agent.parent.get_agents()) > 10

    def should_move(self, agent):
        return random.random() < self.move_probability

    def reproduce(self, a1, a2):
        logger.debug(str(a1) + " " + str(a2) + " reproducing!")
        energy = self.newborn_energy / 2 * 2
        a1.energy -= self.newborn_energy / 2
        a2.add_energy(-self.newborn_energy / 2)
        genotype = a1.crossover.cross(a1.genotype, a2.get_genotype())
        a1.mutation.process([genotype])
        newborn = EmasAgent(genotype, energy)
        a1.parent.locator.add_agent(newborn, get_random_move(a1.parent.locator.get_allowed_moves(a1)))
        a1.parent.add_agent(newborn)


