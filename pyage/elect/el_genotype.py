
class Votes(object):
    def __init__(self, votes, candidate):
        self.votes = [list(h) for h in votes]
        self.fitness = None
        self.candidate = candidate

    def __str__(self):
        return "{0}\nfitness: {1}".format("\n".join(map(str,self.votes)), self.fitness)
        
