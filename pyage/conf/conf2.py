# coding=utf-8
import os
import socket

from pyage.core import address
from pyage.core.agent import  agents_factory
from pyage.core.migration import Pyro4Migration
from pyage.core.operator import Operator
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer
from pyage.solutions.evolution.mutation import PointMutation

workspace_name = lambda: "workspace.t"
agents = lambda: {}

address_provider = address.AddressProvider
ns_hostname = lambda: "max"

migration = Pyro4Migration
