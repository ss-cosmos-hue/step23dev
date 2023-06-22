#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def two_opt(tour, distances):
    N = len(tour)
    for j in range(0, N-3):
        city_a_index_in_tour = j
        city_b_index_in_tour = j + 1
        city_a_id = tour[city_a_index_in_tour]
        city_b_id = tour[city_b_index_in_tour]
        for k in range(j+2, N-1):
            city_c_index_in_tour = k
            city_d_index_in_tour = k + 1
            city_c_id = tour[city_c_index_in_tour]
            city_d_id = tour[city_d_index_in_tour]
            decrease_distance = decrease_when_swap(
                distances, city_a_id, city_b_id, city_c_id, city_d_id)
            if (decrease_distance > 0):
                tour[city_b_index_in_tour:city_c_index_in_tour +
                     1] = tour[city_b_index_in_tour:city_c_index_in_tour+1][::-1]

        if (city_a_index_in_tour >= 1):
            city_c_index_in_tour = N - 1
            city_d_index_in_tour = 0
            city_c_id = tour[city_c_index_in_tour]
            city_d_id = tour[city_d_index_in_tour]

            decrease_distance = decrease_when_swap(
                distances, city_a_id, city_b_id, city_c_id, city_d_id)
            if (decrease_distance > 0):
                tour[city_b_index_in_tour:city_c_index_in_tour +
                     1] = tour[city_b_index_in_tour:city_c_index_in_tour+1][::-1]
    return tour


def decrease_when_swap(distances, city_a_id,  city_b_id,  city_c_id,  city_d_id):
    dist_ab = distances[city_a_id][city_b_id]
    dist_cd = distances[city_c_id][city_d_id]
    dist_ac = distances[city_a_id][city_c_id]
    dist_bd = distances[city_b_id][city_d_id]
    original_edges_length = dist_ab + dist_cd
    new_edges_length = dist_ac + dist_bd
    return original_edges_length - new_edges_length


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
    tour_improved = two_opt(tour, distances=dist)
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
