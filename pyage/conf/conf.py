# coding=utf-8
import os
import socket
import Pyro4

from pyage.core import address
from pyage.core.agent import  agents_factory
from pyage.core.locator import Pyro4Locator
from pyage.core.migration import Pyro4Migration
from pyage.core.operator import Operator
from pyage.solutions.evolution.crossover import AverageCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer
from pyage.solutions.evolution.mutation import UniformPointMutation
from pyage.solutions.evolution.selection import TournamentSelection

agents = agents_factory("max")
step_limit = lambda: 1000

makz__operators = lambda: [Operator()]
max__operators = lambda: [RastriginEvaluation(), TournamentSelection(size=20, tournament_size=10),
                          AverageCrossover(size=100), UniformPointMutation()]
initializer = lambda: PointInitializer(100, -1000, 1000)

address_provider = address.AddressProvider

migration = Pyro4Migration
locator = Pyro4Locator
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

ns_hostname = lambda: "192.168.0.103"
