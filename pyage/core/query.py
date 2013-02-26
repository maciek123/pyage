import Pyro4

def query_property(workspace_name, agent_address, property):
    workspace = Pyro4.Proxy(workspace_name)
    return getattr(workspace.get_agent(agent_address), property)
