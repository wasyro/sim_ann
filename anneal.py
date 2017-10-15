import matplotlib.pyplot as plt
import numpy as np
import math

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
        plt.show()

    return X, Y

def coordinates_to_distance_table(coordinates):
    distance_table = []
    for x1, y1 in coordinates:
        distance_list = []
        for x2, y2 in coordinates:
            distance_list.append(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
        distance_table.append(distance_list)
    return distance_table

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
            nearest_city = path[0]
            path = np.append(path, nearest_city)
        else:
            nearest_distance = np.min(distance_list[np.argwhere(bin_path)])
            nearest_city = int(np.argwhere(distance_list == nearest_distance))

        city = nearest_city
    return path

def showmap(X, Y, path):
    path_sorted_X = []
    path_sorted_Y = []
    for city_num in path:
        path_sorted_X.append(X[city_num])
        path_sorted_Y.append(Y[city_num])
    fig, ax = plt.subplots()
    plt.xlim([-5000, 2000000])
    plt.ylim([-5000, 2000000])
    ax.tick_params(labelbottom='off', bottom='off',
                   labelleft='off', left='off')
    plt.gca().set_aspect('equal', adjustable='box')
    ax.plot(path_sorted_X, path_sorted_Y, marker='o', markersize=8, color='black')
    plt.show()

if __name__ == '__main__':
    X, Y = input_coordinates(showmap=False)
    coordinates = list(zip(X, Y))
    distance_table = coordinates_to_distance_table(coordinates)
    path = greedy_tsp(distance_table)
    showmap(X, Y, path)
