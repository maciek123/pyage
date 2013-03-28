# coding=utf-8
import os
import Pyro4

from pyage.core import address
from pyage.core.agent import    AggregateAgent, unnamed_agents
from pyage.core.emas import EmasService
from pyage.core.locator import  ParentLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import  AverageFloatCrossover
from pyage.solutions.evolution.evaluation import  FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import  float_emas_initializer
from pyage.solutions.evolution.mutation import  UniformFloatMutation


agents = unnamed_agents(4, AggregateAgent)

step_limit = lambda: 1000

aggregated_agents = lambda: float_emas_initializer(10, energy=10, size=500, lowerbound=-100, upperbound=100)

emas = EmasService

minimal_energy = lambda: 2
reproduction_minimum = lambda: 12
migration_minimum = lambda: 12
newborn_energy = lambda: 10

evaluation = FloatRastriginEvaluation
crossover = AverageFloatCrossover
mutation = UniformFloatMutation

address_provider = address.AddressProvider

migration = Pyro4Migration
locator = ParentLocator

ns_hostname = lambda: os.environ['NS_HOSTNAME']
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = SimpleStatistics