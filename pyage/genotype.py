class PointGenotype(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fitness = 0

    def __repr__(self):
        return  "[(%s, %s) %s]" % (self.x, self.y, self.fitness)


