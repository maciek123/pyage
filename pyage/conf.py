import operators
from pyage.address import AddressProvider

addressProvider = lambda: AddressProvider()
population_generator = operators.points_population_generator_factory
op = lambda: [operators.random_selection, operators.random_mutation, operators.rosenbrock_evaluation]
stop_condition = lambda: operators.RandomStopCondition("conf")

myEvent = lambda: operators.event
