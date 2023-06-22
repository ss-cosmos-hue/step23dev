#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input, read_output, total_path_length


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def two_opt(tour, distances, kIteration):
    for _ in range(kIteration):
        updated = False
        N = len(tour)
        N_limit = 10000
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

                if (decrease_distance > 0):
                    tour[city_b_index_in_tour:city_c_index_in_tour +
                         1] = tour[city_b_index_in_tour:city_c_index_in_tour+1][::-1]
                    updated = True
        if updated == False:
            print("no longer updated ", _)
            break
    return tour


def decrease_when_swap(distances, city_a_id,  city_b_id,  city_c_id,  city_d_id):
    dist_ab = distances[city_a_id][city_b_id]
    dist_cd = distances[city_c_id][city_d_id]
    dist_ac = distances[city_a_id][city_c_id]
    dist_bd = distances[city_b_id][city_d_id]
    original_edges_length = dist_ab + dist_cd
    new_edges_length = dist_ac + dist_bd
    return original_edges_length - new_edges_length

# 左上の点のIDを返す


def topleft(cities) -> int:

    def eval_topleft(city):
        # この関数の値が小さいほど、左上に位置していることを表す。
        # 9x+16yを計算するのは、横長の座標系にそぐわせるため。
        return 9*city[0]+16*city[1]

    topleft_most_city = cities[0]
    topleft_most_city_id = 0
    for city_id, city in enumerate(cities):
        if eval_topleft(city) < eval_topleft(topleft_most_city):
            topleft_most_city = city
            topleft_most_city_id = city_id
    return topleft_most_city_id


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
    tour_improved = two_opt(tour, dist, 8)
    return tour_improved


def is_crossing(A, B, C, D):  # (A,B)と(C,D)が交わっていて，(A,C)と(B,D)にしたほうがよいかどうか判断する
    if distance(A, B)+distance(C, D) > distance(A, C)+distance(B, D):
        return True
    return False
    # 交点を求めて，それが線分上にあるかどうか調べるのもありかも


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
