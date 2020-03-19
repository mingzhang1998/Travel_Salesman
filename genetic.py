import math
import random


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_distance(points):
    """

    :param points:
    :return:  calculate the distances among all points
    """
    cost_matrix = []
    rank = len(points)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(points[i], points[j]))
        cost_matrix.append(row)
    return cost_matrix


class Genetic(object):
    def __init__(self, points):
        """

        :param points: coordinates of points
        """
        self.cost_matrix = calculate_distance(points)
        self.population = 20
        self.iter = 100
        self.rank = len(points)
        self.mutation_rate = 0.05

    def _cross_over(self, parent1, parent2):
        """

        :param parent1: one path
        :param parent2:
        :return: return 1 children path
        """
        positions = random.sample([i for i in range(self.rank)], 2)
        a = min(positions)
        b = max(positions)
        cut_1 = [parent1[i] for i in range(a, b)]
        head = [parent2[i] for i in range(0, a)]
        middle = [parent2[i] for i in range(a, b)]
        tail = [parent2[i] for i in range(b, self.rank)]
        temp = tail + head + middle
        temp_cut = [k for k in temp if k not in cut_1]
        cut_1 = cut_1 + temp_cut[0:(self.rank-b)]
        child = temp_cut[(self.rank-b):] + cut_1
        return child

    def _mutation(self, child):
        """

        :param child: a child path that is prepared for mutation
        :return: a mutated path
        """
        positions = random.sample([i for i in range(self.rank)], 2)
        a = min(positions)
        b = max(positions)
        while a < b:
            temp = child[a]
            child[a] = child[b]
            child[b] = temp
            a += 1
            b -= 1
        return child


