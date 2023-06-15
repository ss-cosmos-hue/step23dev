#!/usr/bin/env python3

from common import format_tour, read_input

import solver_greedy
import solver_random
import solver_simulated_annealing

CHALLENGES = 6

def generate_sample_output():
    for i in range(CHALLENGES):
        print(i)
        cities = read_input(f'input_{i}.csv')
        solver = solver_simulated_annealing
        tour = solver.solve(cities)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')



if __name__ == '__main__':
    generate_sample_output()
