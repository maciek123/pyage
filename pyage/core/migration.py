import Pyro4

def migrate_agent(src_workspace_name, dest_workspace_name, address):
    src_workspace = Pyro4.Proxy("PYRONAME:" + src_workspace_name)
    dest_workspace = Pyro4.Proxy("PYRONAME:" + dest_workspace_name)
    dest_workspace.add_agent(src_workspace.remove_agent(address))

