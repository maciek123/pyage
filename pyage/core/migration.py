import Pyro4
from pyage.core.inject import Inject

class Pyro4Migration(object):


    @Inject("ns_hostname")
    def __init__(self):
        super(Pyro4Migration, self).__init__()

    def migrate_agent(self, src_workspace_name, dest_workspace_name, address):
        ns = Pyro4.locateNS(self.ns_hostname)
        src_workspace = Pyro4.Proxy(ns.lookup(src_workspace_name))
        dest_workspace = Pyro4.Proxy(ns.lookup(dest_workspace_name))
        src_workspace.ping()
        dest_workspace.ping()
        dest_workspace.add_agent(src_workspace.remove_agent(address))

