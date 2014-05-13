# coding=utf-8
import logging

from pyage.core import address

from pyage.core.agent.agent import generate_agents, Agent
from pyage.core.locator import RandomLocator
from pyage.core.migration import NoMigration
from pyage.core.statistics import NoStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.evolution.crossover import AverageFloatCrossover
from pyage.solutions.evolution.evaluation import FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import FloatInitializer
from pyage.solutions.evolution.mutation import UniformFloatMutation
from pyage.solutions.evolution.selection import TournamentSelection

logger = logging.getLogger(__name__)

agents_count = 1
logger.debug("EVO, %s agents", agents_count)

agents = generate_agents("agent", agents_count, Agent)

stop_condition = lambda: StepLimitStopCondition(10)

size = 500
operators = lambda: [FloatRastriginEvaluation(), TournamentSelection(size=125, tournament_size=125),
                     AverageFloatCrossover(size=size), UniformFloatMutation(probability=0.1, radius=1)]
initializer = lambda: FloatInitializer(2, size, -10, 10)

address_provider = address.SequenceAddressProvider

migration = NoMigration
locator = RandomLocator

stats = NoStatistics
