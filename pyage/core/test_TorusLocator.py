from nose.tools import raises
from unittest import TestCase
from pyage.core.locator import TorusLocator
import uuid


class TestTorusLocator(TestCase):
    def test_add_agent(self):
        locator = TorusLocator(2, 5)
        agent = DummyAgent()

        locator.add_agent(agent, (0, 1))

        self.assertIsNotNone(locator.get_allowed_moves(agent))

    def test_add_all(self):
        locator = TorusLocator(2, 5)

        locator.add_all([DummyAgent(), DummyAgent()])

        self.assertEqual(len(locator.get_empty_slots()), 8)

    def test_add_agent_random_position(self):
        locator = TorusLocator(2, 5)
        agent = DummyAgent()

        self.assertIsNotNone(locator.get_allowed_moves(agent))

    @raises(KeyError)
    def test_should_not_add_to_occupied_cell(self):
        locator = TorusLocator(2, 5)
        locator.add_agent(DummyAgent(), (0, 1))
        locator.add_agent(DummyAgent(), (0, 1))

    @raises(RuntimeError)
    def test_should_not_add_when_full(self):
        locator = TorusLocator(1, 1)
        locator.add_agent(DummyAgent())
        locator.add_agent(DummyAgent())

    def test_remove_agent(self):
        locator = TorusLocator(5, 6)
        agent = DummyAgent()
        locator.add_agent(agent, (0, 0))
        self.assertNotIn((0, 0), locator.get_empty_slots())

        locator.remove_agent(agent)

        self.assertIn((0, 0), locator.get_empty_slots())

    def test_get_empty_slots(self):
        locator = TorusLocator(2, 5)
        self.assertEqual(locator.get_empty_slots(), [(x, y) for x in range(2) for y in range(5)])

        locator.add_agent(DummyAgent(), (0, 1))
        self.assertFalse((0, 1) in locator.get_empty_slots())

    def test_allowed_moves(self):
        locator = TorusLocator(5, 6)
        agent = DummyAgent()
        locator.add_agent(agent, (0, 0))
        locator.add_agent(DummyAgent(), (1, 1))

        self.assertEquals(locator.get_allowed_moves(agent),
                          {(0, 1), (0, 5), (1, 0), (1, 5), (4, 0), (4, 1), (4, 5)})

    def test_neighbourhood(self):
        locator = TorusLocator(5, 6)
        a1 = DummyAgent()
        a2 = DummyAgent()
        a3 = DummyAgent()
        locator.add_agent(a1, (0, 0))
        locator.add_agent(a2, (0, 1))
        locator.add_agent(a3, (0, 3))

        self.assertEqual(a2, locator.get_neighbour(a1))
        self.assertFalse(a3 == locator.get_neighbour(a1))
        self.assertIsNone(locator.get_neighbour(a3))

    def test_remove_dead_agents(self):
        locator = TorusLocator(5, 6)
        a1 = DummyAgent()
        a2 = DummyAgent()
        locator.add_agent(a1, (0, 0))
        locator.add_agent(a2, (0, 1))

        self.assertEqual(a2, locator.get_neighbour(a1))
        a2.dead = True

        self.assertIsNone(locator.get_neighbour(a1))

    def test_neighbourhood_radius(self):
        locator = TorusLocator(5, 6, 2)
        agent = DummyAgent()
        locator.add_agent(agent, (0, 0))

        self.assertEquals(locator.get_allowed_moves(agent),
                          {(0, 1), (0, 5), (1, 0), (1, 1), (1, 5), (4, 0), (4, 1), (4, 5), (0, 2), (1, 2), (2, 2),
                           (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (4, 2), (0, 4), (1, 4), (2, 4), (2, 5), (4, 4),
                           (3, 4), (3, 5)})

    def test_add_too_many_agents(self):
        locator = TorusLocator(5, 5)
        self.assertEqual(25, locator.add_all([DummyAgent() for _ in range(30)]))

    def test_remove_dead(self):
        locator = TorusLocator(1, 1)
        agent = DummyAgent()
        locator.add_agent(agent, (0, 0))
        agent.dead = True
        locator.add_agent(DummyAgent(), (0, 0))


class DummyAgent(object):
    def __init__(self):
        super(DummyAgent, self).__init__()
        self.address = str(uuid.uuid4().get_hex())

    def get_address(self):
        return self.address
