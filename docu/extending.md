Extending Pyage with new agents
===
You can implement your own agents using arbitrary algorithms to solve problems.

Key part of agent, is **step** method which is invoked once in every computation step. It should contain all important logic. Let's have a look on an example:
```
class Agent(Addressable, AbstractAgent):
    @Inject("migration")
    def __init__(self):
        super(Agent, self).__init__()
        self.population = []
        self.validate_operators()
        self.initialize()

    def step(self):
        for o in self.operators:
            o.process(self.population)
        self.__migrate()


    def __migrate(self):
        self.migration.migrate(self)
```
In most cases, it is a good idea to extend AbstractAgent from Pyage core. It gives you some useful methods like, get_fitness or validate_operatos, so you don't have to implement it every time. It also inject's operators defined in configuration into agent's object.

In our example, we also inject migration component from the configuration. The Inject annotation scans configuration searching component named migration and sets it in a property with the same name. So we can refer to it by typing self.migration.

In step method, we simply iterate over operators and process the population. Finally, we invoke migrate method of the migration component. The decision if the migration should happen is taken by migration object and depends on its implementation.
 
