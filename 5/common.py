import math


def read_input(filename):
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


def read_output(output_file, N):
    with open(output_file) as f:
        lines = f.readlines()
        assert lines[0].strip() == 'index'
        tour = [int(i.strip()) for i in lines[1:N + 1]]
    return tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def total_path_length(tour, cities):
    N = len(tour)
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]])
               for i in range(N))


def format_tour(tour):
    return 'index\n' + '\n'.join(map(str, tour))


def print_tour(tour):
    print(format_tour(tour))
