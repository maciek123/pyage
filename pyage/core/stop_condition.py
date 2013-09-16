class StopCondition(object):
    def should_stop(self, workplace):
        raise NotImplementedError()


class StepLimitStopCondition(StopCondition):
    def __init__(self, step_limit):
        super(StepLimitStopCondition, self).__init__()
        self.step_limit = step_limit

    def should_stop(self, workplace):
        return 0 < self.step_limit <= workplace.steps


class MinimumFitnessStopCondition(StopCondition):
    def __init__(self, minimal_fitness):
        super(MinimumFitnessStopCondition, self).__init__()
        self.minimal_fitness = minimal_fitness

    def should_stop(self, workplace):
        return workplace.get_fitness() >= self.minimal_fitness
