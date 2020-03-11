import random
import math


class Graph(object):
    def __init__(self, points, cost_matrix, rank):
        """

        :param points: list of tuples for the coordinates of points
        :param cost_matrix: matrix of distance among locations, 2d array
        :param rank: number of locations, int
        """
        self.points = points
        self.matrix = cost_matrix
        self.rank = rank
        # initiate a pheromone matrix in which the pheromone density for all paths are the same
        self.pheromone = [[1/(rank * rank) for i in range(rank)] for j in range(rank)]


class ACO(object):
    def __init__(self, num_ants=10, num_itr=100, alpha=1, beta=10, rho=0.5, q=10):
        """

        :param num_ants: number of ants we use in this algorithm, int
        :param num_itr: number of iterations we try, int
        :param alpha: relative importance of pheromone amount, float
        :param beta: relative importance of heuristic, float
        :param rho: evaporation rate of pheromone, float
        :param q: constant Q, float
        """

        self.Q = q
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.num_ants = num_ants
        self.num_itr = num_itr

    def _update_pheromone(self, graph: Graph, ants: list):
        for i in range(graph.rank):
            for j in range(graph.rank):
                graph.pheromone[i][j] *= (1-self.rho)
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    def solve(self, graph):
        """

        :param graph: we take graph as our input
        :return: return the best path and best length after iterations
        """

        best_length = math.inf
        best_path = []
        all_path = []
        all_length = []
        for itr in range(self.num_itr):
            ants = [_Ant(self, graph) for i in range(self.num_ants)]
            for ant in ants:
                for i in range(graph.rank - 1):
                    ant.select_next()
                ant.total_length += graph.matrix[ant.tabu[-1]][ant.tabu[0]]
                if ant.total_length < best_length:
                    best_length = ant.total_length
                    best_path = ant.tabu
                    all_path.append(best_path)
                    all_length.append(best_length)
                ant.update_delta_pheromone()
            self._update_pheromone(graph, ants)

        return best_path, best_length, all_path, all_length


class _Ant(object):
    def __init__(self, aco, graph):
        """

        :param aco: input of the current optimization, ACO
        :param graph: input of the distance and rank, Graph
        """
        self.colony = aco
        self.graph = graph
        self.total_length = 0.0
        self.tabu = []  # a tabu list which tells the ants the location that they have been travelled
        self.pheromone_delta = []  # the increment amount of pheromone at each step
        self.allowed = [i for i in range(graph.rank)]  # a list of available locations an ant can go next time

        #  eta denotes the heuristic value we use in this algorithm, and it will be 1/distance(i,j)
        self.eta = [[0 if i == j else 1/graph.matrix[i][j] for i in range(graph.rank)]for j in range(graph.rank)]

        # initiate an ant with a random starting point
        start = random.randint(0, graph.rank-1)
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)

    def select_next(self):
        """

        :return: make the ant choose its next step, and update the tabu list, allowed list and total length
        """
        # The value of this total_weight is used as the denominator when we are calculating the probability of every
        # possible move.
        total_weight = 0
        for i in self.allowed:
            total_weight += (self.graph.pheromone[self.current][i] ** self.colony.alpha) * (self.eta[self.current][i]
                                                                                   ** self.colony.beta)
        # We are trying to calculate the probability for this ant to move to every location
        probabilities = [0 for i in range(self.graph.rank)]
        for i in range(self.graph.rank):
            try:
                self.allowed.index(i)  # try to see if i is a possible location for the next move
                probabilities[i] = (self.graph.pheromone[self.current][i] ** self.colony.alpha) \
                                   * (self.eta[self.current][i] ** self.colony.beta) / total_weight
            except ValueError:
                pass
        population = [i for i in range(self.graph.rank)]
        selected = random.choices(population, probabilities)[0]
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_length += self.graph.matrix[self.current][selected]
        self.current = selected

    def update_delta_pheromone(self):
        """

        :return: return the increment value of pheromone
        """
        self.pheromone_delta = [[0 for i in range(self.graph.rank)] for j in range(self.graph.rank)]
        for k in range(1, len(self.tabu)):
            last = self.tabu[k-1]
            curr = self.tabu[k]
            self.pheromone_delta[last][curr] = self.colony.Q / self.total_length
