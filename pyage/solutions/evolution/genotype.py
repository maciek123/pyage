class PointGenotype(object):
    def __init__(self, x, y):
        super(PointGenotype, self).__init__()
        self.x = x
        self.y = y
        self.fitness = None

    def __str__(self):
        return "(%s, %s), f:%s" % (self.x, self.y, self.fitness)

    def __repr__(self):
        return self.__str__()



class FloatGenotype(object):
    def __init__(self, genes):
        super(FloatGenotype, self).__init__()
        self.fitness = None
        self.genes = genes

    def __str__(self):
        return "%s, f:%s" % (self.genes, self.fitness)

    def __repr__(self):
        return self.__str__()
