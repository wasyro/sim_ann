import matplotlib.pyplot as plt
import numpy as np
import math
import time
import threading

def input_coordinates(showmap=False):
    with open('prefs.out', 'r') as fin:
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
        plt.xlim([-5000, 2000000])
        plt.ylim([-5000, 2000000])

    return X, Y

def coordinates_to_distance_table(coordinates):
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
    while i < path.size - 1:
        present_idx = path[i]
        next_idx = path[i + 1]
        distance += math.sqrt((X[present_idx] - X[next_idx]) ** 2
                              + (Y[present_idx] + Y[next_idx]) ** 2)
        i += 1
    return distance

def prob_exec(prob):
    if np.random.rand() <= prob:
        return True
    else:
        return False

def random_path():
    path = np.random.permutation(47)
    path = np.append(path, path[0])
    return path

def metropolis(path1, X, Y, distance1, T):
    path2 = np.copy(path1)
    n = path1.size
    swap_cities_idx = np.random.randint(1, n-1, size=2)
    while True:
        if swap_cities_idx[0] == swap_cities_idx[1]:
            swap_cities_idx = np.random.randint(1, n-1, size=2)
        else:
            break

    path2[swap_cities_idx[0]], path2[swap_cities_idx[1]] = \
            path2[swap_cities_idx[1]], path2[swap_cities_idx[0]]

    distance2 = calc_distance(path2, X, Y)
    if distance1 < distance2:
        delta = distance2 - distance1
        prob = math.exp(- delta / T)
        if prob_exec(prob):
            return path2, distance2
        else:
            return path1, distance1
    else:
        return path2, distance2

def greedy_tsp(distance_table):
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
            initial_city = path[0]
            path = np.append(path, initial_city)
        else:
            nearest_distance = np.min(distance_list[np.argwhere(bin_path)])
            nearest_city = int(np.argwhere(distance_list == nearest_distance))

        city = nearest_city
    return path

def anneal(path, X, Y, exec_time=10, T=100, step=1000,
           annealing_schedule=0.995, figure=False):
    path = np.copy(path)
    distance = calc_distance(path, X, Y)
    distances = []
    time_list = []
    time1, time2 = time.time(), time.time()
    while time2 - time1 < exec_time:
        for _ in range(step):
            path, distance = metropolis(path, X, Y, distance, T)
        time_list.append(time2 - time1)
        distances.append(distance)
        T *= annealing_schedule
        time2 = time.time()

    if figure:
        plt.plot(time_list, distances, color='dimgray', lw=1)
    return path

def showmap(path, X, Y):
    path_sorted_X = []
    path_sorted_Y = []
    for city_num in path:
        path_sorted_X.append(X[city_num])
        path_sorted_Y.append(Y[city_num])
    plt.xticks([])
    plt.yticks([])
    plt.plot(path_sorted_X, path_sorted_Y, marker='o',
            markersize=5, color='dimgray', lw=1)

if __name__ == '__main__':
    X, Y = input_coordinates()
    coordinates = list(zip(X, Y))
    distance_table = coordinates_to_distance_table(coordinates)
    path = greedy_tsp(distance_table)

    plt.subplot(121)
    plt.title('Annealing result')
    plt.xlabel('CPU Time')
    plt.ylabel('Tour length (m)')

    path = anneal(path, X, Y, exec_time=60, T=1000000, step=1000,
                  annealing_schedule=0.995, figure=True)
    plt.subplot(122)
    plt.title('Route')
    showmap(path, X, Y)
    plt.show()

    with open('result', 'w') as fout:
        fout.write('path\n')
        for city in path:
            fout.write(str(city) + '\n')
        fout.write('')
