import string
from math import inf


def read_data(file):
    with open(file) as fp:
        data = []
        for i, line in enumerate(fp):
            data.append(list(line.strip()))
    return data


def find_starting_location(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '@':
                return i, j

def find_key_location(data):
    nodes = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in string.ascii_lowercase:
                nodes.append((i, j))
    return nodes

def compute_distance(node1, node2, graph):
    x1, y1 = node1[0], node1[1]
    x2, y2 = node2[0], node2[1]
    dist = 0
    while not (x1 == x2 and y1 == y2):
        if abs(x2 - (x1 + 1)) < abs(x2 - x1) and graph[x1 + 1][y1] != '#':
            x1 += 1
            dist += 1
        elif abs(x2 - (x1 - 1)) < abs(x2 - x1) and graph[x1 - 1][y1] != '#':
            x1 -= 1
            dist += 1
        if abs(y2 - (y1 + 1)) < abs(y2 - y1) and graph[x1][y1 + 1] != '#':
            y1 += 1
            dist += 1
        elif abs(y2 - (y1 - 1)) < abs(y2 - y1) and graph[x1][y1 - 1] != '#':
            y1 -= 1
            dist += 1
    print(dist)
    return dist


def find_shortest_path(data):
    start = find_starting_location(data)
    key_locs = find_key_location(data)
    key_locs = [[*key_loc, False] for key_loc in key_locs]
    current_node = start
    ind = -1
    path_sum = 0
    while not all([key_loc[2] for key_loc in key_locs]):
        min_path_weight = inf
        for i, key_loc in enumerate(key_locs):
            dist = compute_distance(key_loc, current_node, data)
            if not key_loc[2] and dist < min_path_weight:
                min_path_weight = dist
                ind = i
        key_locs[ind][2] = True
        path_sum += min_path_weight
        current_node = key_locs[ind]
    return path_sum






data = read_data('problem19_testdata.txt')
print(data)
print(find_starting_location(data))
print(find_key_location(data))
print(find_shortest_path(data))
