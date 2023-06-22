#!/usr/bin/env python3


from common import read_input, distance, read_output

CHALLENGES = 8


def verify_output():
    for challenge_number in range(CHALLENGES):
        print(f'Challenge {challenge_number}')
        cities = read_input(f'input_{challenge_number}.csv')
        N = len(cities)
        for output_prefix in ('output', 'sample/greedy'):
            output_file = f'{output_prefix}_{challenge_number}.csv'
            tour = read_output(output_file)
            assert set(tour) == set(range(N))
            path_length = sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]])
                              for i in range(N))
            print(f'{output_prefix:16}: {path_length:>10.2f}')
            print()


if __name__ == '__main__':
    verify_output()
