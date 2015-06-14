import logging
from math import sqrt, ceil
import random

logger = logging.getLogger(__name__)


class Locator(object):
    def get_neighbour(self, agent):
        raise NotImplementedError()

    def get_empty_slots(self):
        raise NotImplementedError()

    def add_agent(self, agent, where):
        raise NotImplementedError()

    def add_all(self, agents):
        raise NotImplementedError()

    def remove_agent(self, agent):
        raise NotImplementedError()

    def get_allowed_moves(self, agent):
        raise NotImplementedError()


class TorusLocator(Locator):
    def __init__(self, x=10, y=10, radius=1):
        super(TorusLocator, self).__init__()
        self._grid = [[None for _ in range(y)] for _ in range(x)]
        self.x = x
        self.y = y
        self.radius = radius

    def get_empty_slots(self):
        self._remove_dead()
        return [(x, y) for x in range(self.x) for y in range(self.y) if self._grid[x][y] is None]

    def add_agent(self, agent, where=None):
        if where is None:
            slots = self.get_empty_slots()
            if not slots:
                raise RuntimeError("Could not add agent to full torus!")
            x, y = random.choice(slots)
        else:
            x, y = where
        self._remove_if_dead(x, y)
        if self._grid[x][y] is not None:
            raise KeyError("Position occupied: (%d, %d)" % (x, y))
        self._grid[x][y] = agent
        return x, y

    def add_all(self, agents):
        added = 0
        try:
            for agent in agents:
                self.add_agent(agent)
                added += 1
        except:
            logger.warning("Could not add all agents to torus")
        return added

    def remove_agent(self, agent):
        x, y = self._get_coords(agent)
        self._grid[x][y] = None

    def get_allowed_moves(self, agent):
        x, y = self._get_coords(agent)
        self._remove_dead_neighbours(x, y)
        return set(filter(lambda (x, y): self._grid[x][y] is None, self._get_nieghbour_coords(x, y)))

    def get_neighbour(self, agent):
        try:
            x, y = self._get_coords(agent)
            self._remove_dead_neighbours(x, y)
            neighbours = [self._grid[i][j] for (i, j) in (self._get_nieghbour_coords(x, y)) if
                          self._grid[i][j] is not None]
            return random.choice(neighbours)
        except IndexError:
            return None

    def _get_coords(self, agent):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value == agent:
                    return i, j
        return self.add_agent(agent)

    def _get_nieghbour_coords(self, x, y):
        return [(i % self.x, j % self.y) for i in range(x - self.radius, x + self.radius + 1) for j in
                range(y - self.radius, y + self.radius + 1) if i != x or j != y]

    def _remove_dead(self):
        for i in range(self.x):
            for j in range(self.y):
                self._remove_if_dead(i, j)

    def _remove_dead_neighbours(self, x, y):
        for (i, j) in self._get_nieghbour_coords(x, y):
            self._remove_if_dead(i, j)

    def _remove_if_dead(self, x, y):
        if hasattr(self._grid[x][y], "dead") and self._grid[x][y].dead:
            self._grid[x][y] = None

# old, deprecated classes, kept for compatibility reasons
GridLocator = TorusLocator
RowLocator = TorusLocator
RandomLocator = TorusLocator