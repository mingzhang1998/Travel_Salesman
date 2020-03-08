import matplotlib.pyplot as plt


def plot(points, path):
    """

    :param points: list of tuples for the coordinates of points
    :param path: a sequence of indices denotes the path for the ant
    :return: a plot for path
    """
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x, y, "co")

    for k in range(0, len(path)):
        i = path[k - 1]
        j = path[k]
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()
