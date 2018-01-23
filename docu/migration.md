Migration
===
 ```python -Wignore -m Pyro4.naming -n IP``` 

To run Pyage in distributed mode, [Pyro](https://pypi.python.org/pypi/Pyro4) middleware has been used. It enables remote method invocation:

    +----------+                         +----------+
    |  node A  |                         |  node B  |
    |          |       < network >       |          |
    | Pyage    |                         |   Pyage  |
    | AGENT ---------agent.invoke()--------> AGENT  |
    |          |                         |          |
    +----------+                         +----------+

Migrating agent from one island to other, located on other node is achieved by invoking remotely **add_agent** method. Pyro handles arguments serialization and all network operations.

[Pyro nameserver](http://pythonhosted.org/Pyro4/nameserver.html#nameserver-nameserver) is a registry of all available computing islands and their addresses. Every island registers itself in the nameserver at startup of the node, and deregisters at shutdown.

To be able to locate nameserver, every Pyage node requires nameserver address to be given as a part of the configuration (usually as environmental variable).

This approach makes migrating an agent very simple. The migration component contacts nameserver to get list of available locations for the agent to migrate to. Then remotely invokes **add_agent** method of chosen island to migrate the agent. 
