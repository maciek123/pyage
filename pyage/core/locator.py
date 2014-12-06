import logging
from math import sqrt, ceil
import random

logger = logging.getLogger(__name__)


class Locator(object):
    def get_neighbour(self, agent):
        raise NotImplementedError()

    def get_empty_slots(self):
        raise NotImplementedError()

    def add_agent(self, agent, *where):
        raise NotImplementedError()

    def add_all(self, agents):
        raise NotImplementedError()

    def remove_agent(self, agent):
        raise NotImplementedError()

    def get_allowed_moves(self, agent):
        raise NotImplementedError()


class RandomLocator(Locator):
    def get_neighbour(self, agent):
        siblings = list(agent.parent.get_agents())
        if len(siblings) < 2:
            return None
        siblings.remove(agent)
        return random.choice(siblings)

    def remove_agent(self, agent):
        pass

    def get_allowed_moves(self, agent):
        return super(RandomLocator, self).get_allowed_moves(agent)

    def get_empty_slots(self):
        return super(RandomLocator, self).get_empty_slots()

    def add_all(self, agents):
        return super(RandomLocator, self).add_all(agents)

    def add_agent(self, agent, *where):
        return super(RandomLocator, self).add_agent(agent, where)


class RowLocator(Locator):
    def get_neighbour(self, agent):
        siblings = list(agent.parent.get_agents())
        if len(siblings) < 2:
            return None
        index = siblings.index(agent)
        return random.choice(siblings[index - 2:index] + siblings[index + 1:index + 3])

    def remove_agent(self, agent):
        pass

    def get_allowed_moves(self, agent):
        return super(RowLocator, self).get_allowed_moves(agent)

    def get_empty_slots(self):
        return super(RowLocator, self).get_empty_slots()

    def add_all(self, agents):
        return super(RowLocator, self).add_all(agents)

    def add_agent(self, agent, *where):
        return super(RowLocator, self).add_agent(agent, where)


class GridLocator(Locator):
    def get_neighbour(self, agent):
        siblings = list(agent.parent.get_agents())
        if len(siblings) < 2:
            return None
        index = siblings.index(agent)
        size = len(siblings)
        dim = int(ceil(sqrt(size)))
        return siblings[random.choice([index - dim, index - 1, index + 1, index + dim]) % size]

    def remove_agent(self, agent):
        pass

    def get_allowed_moves(self, agent):
        return super(GridLocator, self).get_allowed_moves(agent)

    def get_empty_slots(self):
        return super(GridLocator, self).get_empty_slots()

    def add_all(self, agents):
        return super(GridLocator, self).add_all(agents)

    def add_agent(self, agent, *where):
        return super(GridLocator, self).add_agent(agent, *where)


class TorusLocator(Locator):
    def __init__(self, x, y):
        super(TorusLocator, self).__init__()
        self._grid = [[None for _ in range(y)] for _ in range(x)]
        self.x = x
        self.y = y

    def get_empty_slots(self):
        return [(x, y) for x in range(self.x) for y in range(self.y) if self._grid[x][y] is None]

    def add_agent(self, agent, x=None, y=None):
        if x is None or y is None:
            x, y = random.choice(self.get_empty_slots())
        if self._grid[x][y] is not None:
            raise KeyError("Position occupied: (%d, %d)" % (x, y))
        self._grid[x][y] = agent
        return x, y

    def add_all(self, agents):
        for agent in agents:
            x, y = random.choice(self.get_empty_slots())
            self.add_agent(agent, x, y)

    def remove_agent(self, agent):
        x, y = self._get_coords(agent)
        self._grid[x][y] = None

    def get_allowed_moves(self, agent):
        self._remove_dead()
        x, y = self._get_coords(agent)
        return set(filter(lambda (x, y): self._grid[x][y] is None, self._get_nieghbour_coords(x, y)))

    def get_neighbour(self, agent):
        try:
            self._remove_dead()
            x, y = self._get_coords(agent)
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
        return [(i % self.x, j % self.y) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2) if i != x or j != y]

    def _remove_dead(self):
        for i in range(self.x):
            for j in range(self.y):
                if hasattr(self._grid[i][j], "dead") and self._grid[i][j].dead:
                    self._grid[i][j] = None
