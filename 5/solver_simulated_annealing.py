#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input, total_path_length
from solver_2opt import decrease_when_swap


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    tour = simulated_annealing(tour, dist, cities, 100, 0.9, 5)
    return tour


def simulated_annealing(initiaL_tour, distances, cities, t_0, c_val, candNum=5,  thresh=0.2):
    N = len(initiaL_tour)

    current_tour = initiaL_tour
    best_tour = initiaL_tour
    t = t_0
    N_limit = 10000  # 500

    while t > thresh:

        # x_current(現在の経路)に対して，2組の辺をひっくり返す変形をすることで，次の経路の候補を得る
        # 近傍からランダムに選ぶ
        tour = current_tour.copy()
        merit_swap_pairs = []

        jrange = range(0, N-2)
        if N > N_limit:
            jrange = random.sample(jrange, N_limit)

        for j in jrange:
            krange = range(j+2, N)
            if N > N_limit:
                krange = random.sample(krange, min(N_limit, len(krange)))
            for k in krange:
                city_a_index_in_tour = j
                city_b_index_in_tour = j + 1
                city_c_index_in_tour = k
                city_d_index_in_tour = (k + 1) % N

                city_a_id = tour[city_a_index_in_tour]
                city_b_id = tour[city_b_index_in_tour]
                city_c_id = tour[city_c_index_in_tour]
                city_d_id = tour[city_d_index_in_tour]

                decrease_distance = decrease_when_swap(
                    distances, city_a_id, city_b_id, city_c_id, city_d_id)

                merit_swap_pairs.append(
                    (decrease_distance, (city_a_index_in_tour, city_b_index_in_tour, city_c_index_in_tour, city_d_index_in_tour)))

        # ランダムに，最k近傍の内の一つを得る
        merit_swap_pairs.sort(reverse=True)
        rand_choice = random.randint(0, min(candNum, len(merit_swap_pairs)-1))
        merit, swap_pair = merit_swap_pairs[rand_choice]
        city_a_index_in_tour, city_b_index_in_tour, city_c_index_in_tour, city_d_index_in_tour = swap_pair
        tour[city_b_index_in_tour:city_c_index_in_tour +
             1] = tour[city_b_index_in_tour:city_c_index_in_tour+1][::-1]

        if merit >= 0:
            current_tour = tour
            if total_path_length(current_tour, cities) < total_path_length(best_tour, cities):
                best_tour = current_tour
        elif random.random() <= math.exp(1) ** (-1/t):
            current_tour = tour
        assert (c_val < 1)
        t = t*c_val
    return best_tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
