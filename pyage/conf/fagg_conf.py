# coding=utf-8
import Pyro4

from pyage.core import address
from pyage.core.agent import  agents_factory, aggregate_agents_factory
from pyage.core.locator import  ParentLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import AverageCrossover, AverageFloatCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation, FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer, FloatInitializer
from pyage.solutions.evolution.mutation import UniformPointMutation, UniformFloatMutation
from pyage.solutions.evolution.selection import TournamentSelection

agents = aggregate_agents_factory("aggregate")
aggregated_agents = agents_factory("max", "makz", "m", "a")
step_limit = lambda: 100

size = 1000
operators = lambda: [FloatRastriginEvaluation(), TournamentSelection(size=150, tournament_size=150),
                          AverageFloatCrossover(size=size), UniformFloatMutation(probability=0.1, radius=1)]
initializer = lambda: FloatInitializer(10, size, -10, 10)

address_provider = address.AddressProvider

migration = Pyro4Migration
locator = ParentLocator

ns_hostname = lambda: "10.22.112.235"
pyro_daemon = Pyro4.Daemon(ns_hostname())
daemon = lambda: pyro_daemon

stats = SimpleStatistics