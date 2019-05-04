import json
import os
import random

dataset_dir = 'data'
result_dir = 'results'

def get_random_solution(dataset):
    N = dataset["N"]
    random_solution = [*range(N)]
    random.shuffle(random_solution)
    solution = []
    weight = 0
    for i in random_solution:
        weight += dataset['g'][i]
        if(weight <= dataset["G"]):
            solution.append(i)
        else:
            break
    return solution

def get_random_bool_solution(dataset):
    random_solution = [0] * dataset["N"]
    solution = get_random_solution(dataset)
    for v in solution:
        random_solution[v] = 1 
    return random_solution

def load_dataset(dataset):
    file_name = f"{dataset}.json"
    with open(os.path.join(dataset_dir, file_name), "r") as f:
        data = json.loads(f.read())
    return data

def flush_result(solution, value, etime, computation_method, dataset):
    result = {"elapsed_time":etime, "solution": solution, "max_value": value}
    res_data = json.dumps(result)
    res_file = f"{result_dir}/{computation_method}/{dataset}.json"
    with open(res_file, "w") as f:
        f.write(res_data)

def process_solution(dataset, index_arr):
    value = 0
    weight = 0
    for i in index_arr:
        weight += dataset['g'][i]
        value += dataset['v'][i]
    if(weight <= dataset["G"]):
        return value, weight
    else:
        return -1, weight

def process_bool_solution(dataset, bool_solution):
    return process_solution(dataset, [x for x, v in enumerate(bool_solution) if v == 1])