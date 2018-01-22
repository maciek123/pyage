# coding=utf-8
import logging
import os
import math

from pyage.core import address

from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.stats.gnuplot import StepStatistics
from pyage.core.stop_condition import StepLimitStopCondition

from pyage.elect.el_crossover import Crossover
from pyage.elect.el_eval import kApprovalEvaluator 
from pyage.elect.el_init import EmasInitializer, root_agents_factory, VotesInitializer
from pyage.elect.el_mutation import Mutation
from pyage.elect.naming_service import NamingService

logger = logging.getLogger(__name__)

chosen_candidate = 2
k_approval_coeff = 2
number_of_cand = 5
number_of_votes = 30
votes, init_c_places = VotesInitializer(number_of_cand,number_of_votes, chosen_candidate,0)()
logger.info("Initial votes:\n%s", "\n".join(map(str,votes)))

votes_nr = len(votes)


agents_count = 2
logger.debug("EMAS, %s agents", agents_count)
agents = root_agents_factory(agents_count, AggregateAgent)

stop_condition = lambda: StepLimitStopCondition(20000)

agg_size = 40
aggregated_agents = EmasInitializer(votes=votes, candidate = chosen_candidate, size=agg_size, energy=40 )

emas = EmasService

minimal_energy = lambda: 10
reproduction_minimum = lambda: 100
migration_minimum = lambda: 120
newborn_energy = lambda: 100
transferred_energy = lambda: 40

budget = 0
evaluation = lambda: kApprovalEvaluator(k_approval_coeff,[simple_cost_func]*votes_nr,budget, init_c_places, chosen_candidate)
crossover = lambda: Crossover(size=30)
mutation = lambda: Mutation(probability=0.2, evol_probability=0.5)

def simple_cost_func(x): return abs(x)*10


address_provider = address.SequenceAddressProvider

migration = ParentMigration
locator = GridLocator

stats = lambda: StepStatistics('fitness_%s_pyage.txt' % __name__)

naming_service = lambda: NamingService(starting_number=2)
