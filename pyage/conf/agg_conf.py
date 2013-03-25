# coding=utf-8
import Pyro4

from pyage.core import address
from pyage.core.agent import  agents_factory, aggregate_agents_factory
from pyage.core.locator import  ParentLocator
from pyage.core.migration import Pyro4Migration
from pyage.solutions.evolution.crossover import AverageCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer
from pyage.solutions.evolution.mutation import UniformPointMutation
from pyage.solutions.evolution.selection import TournamentSelection

agents = aggregate_agents_factory("aggregate")
aggregated_agents = agents_factory("max", "makz")
step_limit = lambda: 1000000

operators = lambda: [RastriginEvaluation(), TournamentSelection(size=20, tournament_size=10),
                          AverageCrossover(size=100), UniformPointMutation()]
initializer = lambda: PointInitializer(100, -1000, 1000)

address_provider = address.AddressProvider

migration = Pyro4Migration
locator = ParentLocator

ns_hostname = lambda: "192.168.0.103"
pyro_daemon = Pyro4.Daemon(ns_hostname())
daemon = lambda: pyro_daemon