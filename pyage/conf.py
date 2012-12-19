# coding=utf-8

#przykładowa konfiguracja dla algorytmu genetycznego

import operators

project_name = 'pyage'

population_generator = operators.points_population_generator_factory
op = lambda: [operators.random_selection, operators.random_mutation, operators.rosenbrock_evaluation]
stop_condition = operators.RandomStopCondition

event_manager = lambda: operators.event
