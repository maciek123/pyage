import random
from pyage.PointGenotype import PointGenotype

def points_population_generator():
    return [PointGenotype(random.random(), random.random()) for _ in range(100)]


def rosenbrock(point):
    x, y = point.x, point.y
    point.fitness = (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
    return point


def rosenbrock_evaluation(population):
    map(lambda point: rosenbrock(point), population)


def random_selection(population):
    for point in population:
        if random.random() < 0.001:
            population.remove(point)


def random_mutation(population):
    for point in population:
        point.x += random.random() * 10 - 5
        point.y += random.random() * 10 - 5


def random_stop_condition(population):
    return random.random() > 0.99
