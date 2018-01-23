How to solve custom problems using Pyage
===

If you want to use Pyage for solving your own problem, you should consider following steps:

Encode problem's solution as genotype.
---
Genotype is an object representing proposed solution to a problem. Example genotype is a Point in 2D space.
```
class PointGenotype(object):
    def __init__(self, x, y):
        super(PointGenotype, self).__init__()
        self.x = x
        self.y = y
        self.fitness = None
```
Implement operators
---
To run genetic algorithms solving your problem, you will need some operators processing genotypes. Operator is just an object with **process** method taking array of genotypes (so called population) as an argument. Operator can specify required type of genotype that it expects by setting **required_type** property. Eg. some operators may operate only on a PointGenotype (defined above), others may be universal (accepting all genotypes). Pyage will perform type checking before using operators during computation.

Evaluation operator is probably the most important one. It ranks solutions encoded as genotypes by assigning fitness value, the higher fitness value the better the solution is.

This is an example of evaluation operator accepting only PointGenotype and ranking points by assigning De Jong function value.
```
class DeJongEvaluation(Operator):
    def __init__(self, type=None):
        super(DeJongEvaluation, self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__DeJong(genotype.x, genotype.y)

    def __DeJong(self, x, y):
        return x ** 2 + y ** 2
```
For more example operators source code, browse the [repository](https://github.com/macwozni/pyage).

Once you have your genotype and operators ready, you can use them in your computation by putting in Pyage configuration files 
