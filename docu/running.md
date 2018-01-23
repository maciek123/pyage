Running Pyage in distributed mode
===
Pyage can be run in distributed mode. It can be done in following steps:

- make sure all machines can open connection to each other (no blocking iptables etc.)
- on one of the machines run Pyro nameserver: ```python -Wignore -m Pyro4.naming -n IP``` IP should be replaced with actual IP address of this machine. We will refer to it as NS_IP.
- on all machines:
1. set NS_HOSTNAME env. variable to value of NS_IP (ip of nameserver)
2. set PYRO_HOST variable to ip of current machine
3. Make sure to use ```migration = PyroMigration``` in your cofig module
4. Run it as always: ```python -m pyage.core.bootstrap CONF``` replacing conf with your config module

Example config file
---

Example configuration for running EMAS in distributed mode:
```
# coding=utf-8
import os
import Pyro4

from pyage.core import address
from pyage.core.agent.agent import unnamed_agents
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import TorusLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import TimeStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.evolution.crossover import SinglePointCrossover
from pyage.solutions.evolution.evaluation import FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import float_emas_initializer
from pyage.solutions.evolution.mutation import UniformFloatMutation

agents_count = 5
agents = unnamed_agents(agents_count, AggregateAgent)
stop_condition = lambda: StepLimitStopCondition(100)
aggregated_agents = lambda: float_emas_initializer(40, energy=100, size=50, lowerbound=-10, upperbound=10)
emas = EmasService

minimal_energy = lambda: 0
reproduction_minimum = lambda: 90
migration_minimum = lambda: 120
newborn_energy = lambda: 100
transferred_energy = lambda: 40

evaluation = FloatRastriginEvaluation
crossover = SinglePointCrossover
mutation = lambda: UniformFloatMutation(probability=1, radius=1)
address_provider = address.SequenceAddressProvider

migration = Pyro4Migration

locator = TorusLocator
ns_hostname = lambda: os.environ['NS_HOSTNAME']
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = TimeStatistics
```
To learn implementaion details of migrating agents while running in distributed mode, read [Migration](./migration.md) page. 
