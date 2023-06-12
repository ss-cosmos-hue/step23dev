#!/usr/bin/env python3

import sys
import math

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
        #if there will be a crossing, swap path
        if len(tour)>=3:
            for i in range(len(tour)-1):
                #crossしているか，厳密に判定してもOK
                # crossしている方が短いこともあるので，距離のみを比較する
                if is_crossing(cities[tour[i]],cities[tour[i+1]],cities[tour[-1]],cities[next_city]):
                    tour[i+1:] = reversed(tour[i+1:])#swapO(n)
        tour.append(next_city)
        current_city = next_city
    return tour

def is_crossing(A,B,C,D):#(A,B)と(C,D)が交わっていて，(A,C)と(B,D)にしたほうがよいかどうか判断する
    if distance(A,B)+distance(C,D)>distance(A,C)+distance(B,D):
        return True 
    return False
    #交点を求めて，それが線分上にあるかどうか調べるのもありかも


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
