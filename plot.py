import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def plot(points, path, length=0):
    """

    :param points: list of tuples for the coordinates of points
    :param path: a sequence of indices denotes the path for the ant
    :return: a plot for a single path
    """
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x, y, "co")
    if length != 0:
        plt.title("Total length of "+str(int(length)))
    for k in range(0, len(path)):
        i = path[k - 1]
        j = path[k]
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()


def plot_animation(points, path, length, algorithm = "Ant Colony Optimization"):
    """

    :param points: list of tuples for the coordinates of points
    :param path: a sequence of indices denotes the path for the ant
    :return: return an animation of a certain graph
    """
    new_points = []
    for k in path:
        new_points.append(points[k])
    x = []
    y = []
    for point in new_points:
        x.append(point[0])
        y.append(point[1])
    fig = plt.figure()
    ax = plt.axes(xlim=(0, max(x) * 1.1), ylim=(0, max(y) * 1.1))
    plt.plot(x[0], y[0], "ro")
    plt.plot(x[1:], y[1:], "co")
    plt.title(algorithm+ ", total length = "+str(int(length)))
    line, = ax.plot([], [], lw=3)

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        if i<len(points):
            xdata = np.asarray(x[:i])
            ydata = np.asarray(y[:i])
        else:
            xdata = np.append(np.asarray(x), np.array(x[0]))
            ydata = np.append(np.asarray(y), np.array(y[0]))
        line.set_data(xdata, ydata)
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(points)+2, interval=200, blit=True)
    plt.show()


def plot_all(points, all_path, all_length, algorithm):
    """

    :param points:
    :param all_path:
    :param all_length:
    :return: the final dynamic graph
    """
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 10000), ylim=(0, 10000))
    line, = ax.plot([],[],lw=3)

    def init():
        line.set_data([], [])
        return line,

    def _generate_coordinate(num):
        new_points = []
        for k in all_path[num]:
            new_points.append(points[k])
        x = []
        y = []
        for point in new_points:
            x.append(point[0])
            y.append(point[1])
        return x,y

    def animate(i):
        xdata, ydata = _generate_coordinate(i)
        xdata.append(xdata[0])
        ydata.append(ydata[0])
        line.set_data(xdata, ydata)
        plt.title(algorithm + ", total length = " + str(int(all_length[i])))
        return line,
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(all_path), interval=50, repeat=False)
    plt.show()

