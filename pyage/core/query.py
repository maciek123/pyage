import Pyro4

def query_property(workspace_name, agent_address, property):
    workspace = Pyro4.Proxy("PYRONAME:" + workspace_name)
    agent = workspace.get_agent(agent_address)
    return getattr(agent, property)
