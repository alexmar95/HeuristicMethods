import time
import resutils

dataset = "d100"
computation_method = 'neighborhood_search'


def neghboring_solution(solution):
    for i in range(len(solution)):
        solution[i] ^= 1
        yield(solution)
        solution[i] ^= 1

#Find the best solution from the neighboring solutions
def ns_extended(dataset):
    N = dataset["N"]
    solution_b = [0] * N
    solution = resutils.get_random_solution(dataset)
    for idx in solution:
        solution_b[idx] = 1
    max_value = 0
    search = True
    while(search):
        #print(f"Keep {solution_b} with value:{max_value}")
        sol_generator = neghboring_solution(solution_b)
        search = False
        for sol_candidate in sol_generator:
            index_solution = [idx for idx, v in enumerate(sol_candidate) if v == 1]
            value, _ = resutils.process_solution(dataset, index_solution)
            if( value > max_value):
                solution = index_solution
                solution_b = sol_candidate.copy()
                max_value = value
                search = True
    return solution, max_value

def main():
    ldataset = resutils.load_dataset(dataset)
    start = time.time()
    solution, value = ns_extended(ldataset)
    stop = "%.16f" % (time.time() - start)
    resutils.flush_result(solution, value, stop, computation_method, dataset)

if __name__ == '__main__':
    main()