import time
import resutils
import collections

dataset_name = "d100"
computation_method = 'tabu_search'

tabu_tenure_1 = 3
tabu_tenure_2 = 7
tabu_tenure_3 = 12
tabu_tenure_4 = 20
tabu_tenure =tabu_tenure_1+2
tabu_iterations = 10000

class TabuSearch:
    def __init__(self, tabu_tenure, iterations):
        self._current_solution = resutils.get_random_bool_solution(dataset)
        self._best_solution =  self._current_solution
        self._best_value, self._best_weight = resutils.process_bool_solution(dataset, self._best_solution)
        self._current_value = self._best_value
        self._tabu_list = collections.deque([])
        self._tabu_tenure = tabu_tenure
        self._iterations = iterations

    def get_neghboring_solution(self, solution):
        for i in range(len(solution)):
            solution[i] ^= 1
            yield(solution, i)
            solution[i] ^= 1

    def check_if_tabu(self, move_index):
        return move_index in self._tabu_list

    #returns best solution
    def get_best_solution(self):
        best_solution = None
        best_move_index = None
        best_solution_is_tabu = False
        nontabu_best_value = -1
        best_value = self._best_value
        for sol, move_index in self.get_neghboring_solution(self._current_solution):
            value, _ = resutils.process_bool_solution(dataset, sol)
            sol_is_tabu = self.check_if_tabu(move_index)
            if value > best_value:
                best_solution = sol
                best_move_index = move_index
                best_value = value
                nontabu_best_value = value
                best_solution_is_tabu = sol_is_tabu
            elif not sol_is_tabu and value > nontabu_best_value:
                nontabu_best_value = value
                best_solution = sol
                best_move_index = move_index
        return best_solution, best_move_index, nontabu_best_value, best_solution_is_tabu


    def start(self):
        print(f"Starting tabu serch with tenure:{self._tabu_tenure} and iterations:{self._iterations}")
        for i in range(self._iterations):
            self._current_solution, move_index, self._current_value, is_tabu = self.get_best_solution()
            if not self._current_solution:
                print(f"Can't find valid, non-tabu solutions after {i} iterations")
                break
            if self._current_value > self._best_value:
                self._best_value = self._current_value
                self._best_solution = self._current_solution
            if not is_tabu:
                self._tabu_list.appendleft(move_index)
                if len(self._tabu_list) > self._tabu_tenure:
                    self._tabu_list.pop()

    @property
    def best_solution(self):
        return self._best_solution
    
    @property
    def best_value(self):
        return self._best_value
    
    def __str__(self):
        index_solution = [idx for idx, v in enumerate(self._best_solution) if v == 1]
        return f"{{BestValue:{self._best_value};BestWeight:{self._best_weight};BestSolution:{index_solution}}}"

def main():
    global dataset
    dataset = resutils.load_dataset(dataset_name)
    start = time.time()
    ts = TabuSearch(tabu_tenure, tabu_iterations)
    print(ts)
    ts.start()
    stop = "%.16f" % (time.time() - start)
    solution, value = ts.best_solution, ts.best_value
    index_solution = [idx for idx, v in enumerate(solution) if v == 1]
    print(ts)
    resutils.flush_result(index_solution, value, stop, computation_method, dataset_name)

if __name__ == '__main__':
    main()