import operators
from pyage.AddressProvider import AddressProvider
from pyage.events import EventHook

print "parsing config"

population_generator = operators.points_population_generator
op = [operators.random_selection, operators.random_mutation, operators.rosenbrock_evaluation]
stop_condition=operators.random_stop_condition


addressProvider = AddressProvider()
myEvent = EventHook()
