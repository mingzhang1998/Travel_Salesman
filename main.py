import math
from ACO import ACO, Graph
from plot import plot_all
from plot import plot_animation
from annealing import SimAnneal


def distance(point1, point2):
    return math.sqrt((point1['x'] - point2['x']) ** 2 + (point1['y'] - point2['y']) ** 2)


def run_aco(data="./data/data_20.txt"):
    points = []
    locations = []
    with open(data) as f:
        for line in f.readlines():
            character = line.split(" ")
            locations.append(dict(index=int(character[0]), x=float(character[1]), y=float(character[2])))
            points.append((float(character[1]), float(character[2])))

    cost_matrix = []
    rank = len(points)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(locations[i], locations[j]))
        cost_matrix.append(row)
    aco = ACO(5, 10)
    graph = Graph(points, cost_matrix, rank)
    path, length, all_path, all_length = aco.solve(graph)
    print('length: {}, path: {}'.format(length, path))
    print(all_length)
    plot_all(points, all_path, all_length, algorithm="Ant Colony Algorithm")
    plot_animation(points, path, length)


def run_anneal(data="./data/data_20.txt"):
    points = []
    locations = []
    with open(data) as f:
        for line in f.readlines():
            character = line.split(" ")
            locations.append(dict(index=int(character[0]), x=float(character[1]), y=float(character[2])))
            points.append((float(character[1]), float(character[2])))

    sa = SimAnneal(points, stopping_iter=3000)
    sa.anneal()
    print("best path: ", sa.best_solution, "total length: ", sa.best_fitness)
    plot_all(points, sa.solution_list, sa.fitness_list, "Simulated Annealing")
    plot_animation(points, sa.best_solution, sa.best_fitness)

if __name__ == '__main__':
    # Switch between different algorithms on the same points

    run_aco()
    #run_anneal()