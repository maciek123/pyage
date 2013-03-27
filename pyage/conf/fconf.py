# coding=utf-8
import Pyro4

from pyage.core import address
from pyage.core.agent import  agents_factory
from pyage.core.locator import Pyro4Locator
from pyage.core.migration import  NoMigration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import  AverageFloatCrossover
from pyage.solutions.evolution.evaluation import  FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import  FloatInitializer
from pyage.solutions.evolution.mutation import  UniformFloatMutation
from pyage.solutions.evolution.selection import TournamentSelection

agents = agents_factory("max")
step_limit = lambda: 1000

size = 1000
max__operators = lambda: [FloatRastriginEvaluation(), TournamentSelection(size=250, tournament_size=250),
                          AverageFloatCrossover(size=size), UniformFloatMutation(probability=0.1, radius=1)]
initializer = lambda: FloatInitializer(10, size, -10, 10)

address_provider = address.AddressProvider

migration = NoMigration
locator = Pyro4Locator

ns_hostname = lambda: "192.168.0.103"
pyro_daemon = Pyro4.Daemon(ns_hostname())
daemon = lambda: pyro_daemon
stats = SimpleStatistics
