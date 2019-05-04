import json
import os
import itertools
import time
import resutils
computation_method = 'backtracking'
dataset = "d8"


def backtracking(dataset):
    max_value = 0
    solution = []
    N = dataset["N"]
    for x in range(1, N + 1):
        for index_arr in itertools.combinations(range(N), x):
            value = resutils.calculate_value(dataset, index_arr)
            if value > max_value:
                max_value = value
                solution = index_arr
    return solution, max_value

def main():
    _dataset = resutils.load_dataset(dataset)
    start = time.time()
    solution, value = backtracking(_dataset)
    stop = "%.16f" % (time.time() - start)
    print(f"Done in {stop}")
    print(f'Solution = {solution}')
    print(f"Value = {value}")
    resutils.flush_result(solution, value, stop, computation_method, dataset)

if __name__ == '__main__':
    main()