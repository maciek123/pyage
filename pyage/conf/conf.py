# coding=utf-8
import os
import socket

from pyage.core import address
from pyage.core.agent import Agent, agents_factory

workspace_name = lambda: "workspace." + socket.gethostname() + "." + str(os.getpid())
agents = agents_factory("makz", "max")

address_provider = address.AddressProvider
operators = lambda: []
