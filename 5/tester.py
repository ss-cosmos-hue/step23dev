import solver_greedy
import solver_2opt
import input_generator
import output_verifier
from common import total_path_length


# count = 0
# N = 20
while True:
    # count += 1
    N = 20
    count = 79
    cities = [(x, y) for x, y in input_generator.generate_cities(N, count)]
    tour_greedy = solver_greedy.solve(cities)
    tour_2opt = solver_2opt.solve(cities)
    distance_greedy = total_path_length(tour_greedy, cities)
    distance_2opt = total_path_length(tour_2opt, cities)

    # if count % 10 == 0:
    #     print(count, distance_greedy, distance_2opt)
    # if distance_greedy >= distance_2opt:
    #     continue
    # else:

    print("count,random seed", count)
    print(cities)
    print(tour_greedy, tour_2opt)
    print(distance_greedy, distance_2opt)
    break
