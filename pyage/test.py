import sys
import Pyro4
import Pyro4.util
from pyage.core.agent import Agent

from pyage.core.query import query_property
from pyage.core.migration import migrate_agent

sys.excepthook = Pyro4.util.excepthook


print query_property("workspace.Max.4811", "makz", "fitness")
#migrate_agent("workspace.Max.3251", "workspace", "makz")
print "!"
