# coding=utf-8
import Pyro4

from pyage.core import address
from pyage.core.agent import  agents_factory, aggregate_agents_factory
from pyage.core.locator import  ParentLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import AverageCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer
from pyage.solutions.evolution.mutation import UniformPointMutation
from pyage.solutions.evolution.selection import TournamentSelection

agents = aggregate_agents_factory("aggregate")
aggregated_agents = agents_factory("max", "makz", "m")
step_limit = lambda: 1000

operators = lambda: [RastriginEvaluation(), TournamentSelection(size=50, tournament_size=50),
                     AverageCrossover(size=100), UniformPointMutation(0.3, 100)]
initializer = lambda: PointInitializer(100, -100, 100)

address_provider = address.AddressProvider

migration = Pyro4Migration
locator = ParentLocator

ns_hostname = lambda: "192.168.0.103"
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = SimpleStatistics