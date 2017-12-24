import matplotlib.pyplot as plt
import numpy as np
import math
import time
import sys
from drawnow import drawnow

def input_coordinates(filename, showmap=False):
    with open(filename, 'r') as fin:
        X = []
        Y = []
        while True:
            line = fin.readline()
            if not line:
                break
            x, y = line.split(', ')
            x, y = float(x), float(y)
            X.append(x)
            Y.append(y)

    if showmap:
        plt.scatter(X, Y)

    return X, Y

def _coordinates_to_distance_table(coordinates):
    distance_table = []
    for x1, y1 in coordinates:
        distance_list = []
        for x2, y2 in coordinates:
            distance_list.append(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
        distance_table.append(distance_list)
    return distance_table

def calc_distance(path, X, Y):
    distance = 0
    i = 0
    if isinstance(path, np.ndarray):
        n_iter = path.size - 1
    else:
        n_iter = len(path) - 1

    while i < n_iter:
        present_idx = path[i]
        next_idx = path[i + 1]
        distance += math.sqrt((X[present_idx] - X[next_idx]) ** 2
                              + (Y[present_idx] - Y[next_idx]) ** 2)
        i += 1
    distance += math.sqrt((X[0] - X[-1]) ** 2
                            + (Y[0] - Y[-1]) ** 2)
    return distance

def _prob_exec(prob):
    if np.random.rand() <= prob:
        return True
    else:
        return False

def random_path(X, Y):
    if len(X) != len(Y):
        sys.stderr.write('X and Y are not same length')
    n = len(X)
    path = np.random.permutation(n)
    return path

def _metropolis(path1, X, Y, T):
    distance1 = calc_distance(path1, X, Y)
    path2 = np.copy(path1)
    n = path1.size

    swap_cities_idx = np.random.randint(0, n, size=2)

    path2[swap_cities_idx[0]], path2[swap_cities_idx[1]] = \
            path2[swap_cities_idx[1]], path2[swap_cities_idx[0]]

    distance2 = calc_distance(path2, X, Y)
    if distance2 < distance1:
        return path2, distance2

    delta = distance2 - distance1
    prob = math.exp(- delta / T)
    if _prob_exec(prob):
        return path2, distance2
    else:
        return path1, distance1

def greedy_tsp(X, Y):
    coordinates = list(zip(X, Y))
    distance_table = _coordinates_to_distance_table(coordinates)
    distance_table = np.array(distance_table)
    num_of_cities = len(distance_table)
    city = np.random.randint(0, num_of_cities)
    path = np.array([], dtype='int8')
    bin_path = np.ones([num_of_cities], dtype=bool)
    falses = np.zeros([num_of_cities], dtype=bool)

    for i in range(num_of_cities):
        path = np.append(path, city)
        bin_path[path[i]] = False
        distance_list = distance_table[city]
        if (bin_path == False).all():
            pass
        else:
            nearest_distance = np.min(distance_list[np.argwhere(bin_path)])
            nearest_city = int(np.argwhere(distance_list == nearest_distance))

        city = nearest_city
    return path

def anneal(path, X, Y, n_iter=100000, pmelt=0.7, tgt=0.01, stagfactor=0.05,
           procplt=False, realtime=False, color='dimgray', lw=2):
    n_cities = len(path)
    initial_distance = calc_distance(path, X, Y)
    min_distance, max_distance = initial_distance, initial_distance

    optimized_distances = []
    distances = []
    optimized_distances.append(initial_distance)
    distances.append(initial_distance)
    for i in range(max([0.01 * n_cities, 2])):
        path_, distance = _metropolis(path, X, Y, 10 ** 10)
        if distance < min_distance:
            min_distance = distance
        if max_distance < distance:
            max_distance = distance

    range_ = (max_distance - min_distance) * pmelt
    temp = tgt ** (1 / n_iter)
    optimized_distance = initial_distance
    optimized_step = 1
    optimized_path = path
    path_ = np.copy(path)

    for i in range(1, n_iter):
        if realtime:
            drawnow(showmap, path=path_, X=X, Y=Y)

        sys.stdout.write('\r{} / {} processing...'.format(
                            i + 1, n_iter))
        sys.stdout.flush()

        T = range_ * (temp ** i)
        path_, distance = _metropolis(path_, X, Y, T)

        if distance < optimized_distance:
            optimized_distance = distance
            optimized_path = path_
            optimized_step = i
        optimized_distances.append(optimized_distance)
        distances.append(distance)

        # Reheat
        if i - optimized_step == stagfactor * n_iter:
            temp = temp ** (0.05 * i / n_iter)

    if procplt:
        plt.plot(distances, color='dimgray', lw=1)
        plt.plot(optimized_distances, color='black', lw=2)

    return optimized_path

def showmap(path, X, Y):
    path_sorted_X = [X[city_num] for city_num in path]
    path_sorted_Y = [Y[city_num] for city_num in path]
    path_sorted_X.append(path_sorted_X[0])
    path_sorted_Y.append(path_sorted_Y[0])
    plt.xticks([])
    plt.yticks([])
    plt.plot(path_sorted_X, path_sorted_Y, marker='o',
            markersize=8, color='dimgray', lw=2)

if __name__ == '__main__':
    # this random seed provides better result
    np.random.seed(1000384)
    X, Y = input_coordinates("prefs.out")
    #init_path = greedy_tsp(X, Y)
    init_path = random_path(X, Y)
    
    path = anneal(init_path, X, Y, n_iter=100000, procplt=False, realtime=True)
