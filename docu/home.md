Home
=====

Pyage is agent-based platform for running evolutionary computations, written in python.

Installation and running
----
Pyage runs on Python 2.X.

Pyage is hosted on [pypi](https://pypi.python.org/pypi/pyage), so you can install it using easy_install or pip command-line tool.
```
 pip install pyage
```

Verify your installation with: ```python -m pyage.core.bootstrap pyage.conf.test_conf``` It should run an example config built into pyage. Inspect pyage logfile for any errors.
 
To run EMAS, use ```pyage.conf.femas_single``` as the parameter, but make sure to set AGENTS environment variable to indicate how many aggregate-agents (islands) you want to run.

Running your own configuration
---
Configuration module can be located anywhere in your system, so you can write your own config files. Config module should be visible on PYTHONPATH, and passed as argument to ```pyage.core.bootstrap``` (see above example).

To create your own configuration, you should start with copy of one of [built-in configuration sets](https://github.com/macwozni/pyage/tree/master/pyage/conf), then you can play with parameters.

Example configuration for EMAS would be:
```
from pyage.core import address
from pyage.core.agent.agent import unnamed_agents
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridParentLocator
from pyage.core.migration import ParentMigration
from pyage.core.stats.gnuplot import TimeStatistics, StepStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.evolution.crossover import SinglePointCrossover
from pyage.solutions.evolution.evaluation import FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import float_emas_initializer
from pyage.solutions.evolution.mutation import UniformFloatMutation

agents_count = lambda: 5
agents = unnamed_agents(agents_count, AggregateAgent)

stop_condition = lambda: StepLimitStopCondition(1000)

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

migration = ParentMigration
locator = GridParentLocator

stats = StepStatistics
```
Parameters you may want to change:

- **agents_count** is the number of islands
- **float_emas_initializer(40, energy=100, size=50, lowerbound=-10, upperbound=10)** determines initial configuration inside every islands: 40 is size of the genotype, energy is initial value of agents energy, size is equal to number of agents initially placed on each island, and last two parameters denote range for random initial values into genotypes

Further reading
---
- [How to solve custom problems using Pyage](./howto.md)
- [Implementing your own components](./implementing.md)
- [Extending Pyage with new agents](./extending.md)
- [Running Pyage in distributed mode](./running.md) 
