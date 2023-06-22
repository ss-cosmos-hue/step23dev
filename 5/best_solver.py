from solver_simulated_annealing import simulated_annealing
from solver_2opt import two_opt, topleft
from common import distance


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = topleft(cities)
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    tour_improved = two_opt(tour, cities, dist, 8)
    t_0 = 30
    c_val = 0.5
    thresh = 0.1
    tour_improved_second = simulated_annealing(
        tour_improved, t_0, c_val, cities, thresh)
    return tour_improved_second
