#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input


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
        # if there will be a crossing, swap path
        if len(tour) >= 3:
            for i in range(len(tour)-1):
                # crossしているか，厳密に判定してもOK
                # crossしている方が短いこともあるので，距離のみを比較する
                if is_crossing(cities[tour[i]], cities[tour[i+1]], cities[tour[-1]], cities[next_city]):
                    tour[i+1:] = reversed(tour[i+1:])  # swapO(n)
        tour.append(next_city)
        current_city = next_city
    tour = simulated_annealing(tour, 20, 0.8, cities)
    return tour


def simulated_annealing(x_0, t_0, c_val, cities, thresh=0.01):
    x_current = x_0
    n = len(x_current)

    x_best = x_0
    t = t_0
    candnum = 5
    while t > thresh:
        # x_current(現在の経路)に対して，2組の辺をひっくり返す変形をすることで，次の経路の候補を得る
        # 近傍からランダムに選ぶ
        x = x_current.copy()
        x += x  # 全てのエッジの組み合わせを走査できるように
        edges_to_swap = []
        swap_merits = []
        nx = len(x)
        skip = 5
        for b in range(1, n-2, skip):  # O(n^2)#いくつかにケースを限定してもよいのかもしれない
            for c in range(b+1, b+n, skip):
                a = b-1
                d = c + 1
                edges_to_swap.append((a, b, c, d))
                swap_merits.append(swap_merit(
                    cities[x[a]], cities[x[b]], cities[x[c]], cities[x[d]]))

        # for i in range(candnum):
        #     b,c = random.sample(range(1,n-1),2)
        #     a = b-1
        #     d = c+ 1
        #     edges_to_swap.append((a,b,c,d))
        #     swap_merits.append(swap_merit(cities[x[a]],cities[x[b]],cities[x[c]],cities[x[d]]))

        # ランダムに，最k近傍の内の一つを得る
        zip_merit_edges = zip(swap_merits, edges_to_swap)
        zip_sort = sorted(zip_merit_edges, reverse=True)
        rand_choice = random.randint(0, min(candnum, len(edges_to_swap)-1))
        # print(zip(*(zip_sort[rand_choice])) )
        swap_merits, edges_to_swap = zip(*zip_sort)
        a, b, c, d = list(edges_to_swap)[rand_choice]
        merit = swap_merits[rand_choice]
        x[b:c+1] = x[b:c+1][::-1]  # b~cの経路をひっくり返す

        # nx == n+3
        k = max(0, c+1-n)
        x = x[k:b]+x[b:c+1]+x[c+1:n+k]  # 0<=k<=b,c+1-n<=k<=n

        if merit >= 0:
            x_current = x
            if whole_distance(x, cities) < whole_distance(x_best, cities):
                x_best = x
        elif random.random() <= math.exp(1) ** (-d/t):
            x_current = x
        assert (c_val < 1)
        t = t*c_val
    return x_best


def whole_distance(path, cities):
    dist = 0
    for i in range(len(path)-1):
        dist += distance(cities[path[i]], cities[path[i+1]])
    dist += distance(cities[path[0]], cities[path[-1]])
    return dist


def is_crossing(A, B, C, D):  # city(A,B)と(C,D)が交わっていて，(A,C)と(B,D)にしたほうがよいかどうか判断する
    if distance(A, B)+distance(C, D) > distance(A, C)+distance(B, D):
        return True
    return False
    # 交点を求めて，それが線分上にあるかどうか調べるのもありかも


def swap_merit(A, B, C, D):
    # A,B,C,DからA,C,B,Dにするとき
    return distance(A, B)+distance(C, D)-(distance(A, C)+distance(B, D))


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
