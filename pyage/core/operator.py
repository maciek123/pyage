
class Operator(object):
    def __init__(self, type=None):
        super(Operator, self).__init__()
        self.required_type = type

    def process(self, population):
        raise NotImplementedError()

    def is_compatible(self, operator):
        return  self.required_type == None\
                or operator.required_type == None\
                or operator.required_type == self.required_type