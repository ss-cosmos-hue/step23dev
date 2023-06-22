from solver_simulated_annealing import simulated_annealing
from solver_2opt import two_opt, topleft
from common import distance, read_output, read_input


def solve(cities, initiate_with_file=False, challenge_num=0):
    tour = None
    N = len(cities)

    # 都市間の距離を求める。
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    if initiate_with_file:
        output_file = f'sa_original/output_{challenge_num}.csv'
        tour = read_output(output_file, N)
    else:

        # 焼き鈍し法のパラメタを設定する。
        t_0 = 80
        c_val = 0.9
        thresh = 0.2
        candNum = 8

        # 左上の点を始点とする。
        current_city = topleft(cities)
        unvisited_cities = set(range(0, N))
        unvisited_cities.remove(current_city)
        tour = [current_city]

        # 走査する。
        while unvisited_cities:
            next_city = min(unvisited_cities,
                            key=lambda city: dist[current_city][city])
            unvisited_cities.remove(next_city)
            tour.append(next_city)
            current_city = next_city
    # print("under two opt")
    # tour_two_opt = two_opt(tour, dist, 8)
    print("under sa")
    tour = simulated_annealing(
        tour, dist, cities, t_0, c_val, candNum, thresh)
    print("under two opt")
    tour_two_opt = two_opt(tour, dist, 8)
    return tour_two_opt
