import random
import time
import resutils as ru

computation_method = 'genetic_algorithm'
dataset_name = "d8"

genetic_hyperparameters_arr = [
    {
        "population_size" : 10,
        "no_iterations" : 200,
        #"crossover_rate" : 0.7, #unused
        "mutation_rate" : 0.2,
        "coloning_rate" : 0.1
    },
    {
        "population_size" : 100,
        "no_iterations" : 2000,
        #"crossover_rate" : 0.85, #unused
        "mutation_rate" : 0.1,
        "coloning_rate" : 0.05
    },
    {
        "population_size" : 200,
        "no_iterations" : 1000,
        #"crossover_rate" : 0.7, #unused
        "mutation_rate" : 0.3,
        "coloning_rate" : 0.1
    }
]

class Chromosome:
    def __init__(self, genes):
        self._genes = genes
        self.compute_fit_value()

    @property
    def genes(self):
        return self._genes

    @property
    def fit_value(self):
        return self._fit_value
    
    def __str__(self):
        return f"{{FitValue:{self._fit_value};Weight:{self._weight};Data:{self._genes}}}"

    def is_valid(self):
        return self._fit_value != -1

    def compute_fit_value(self):
        self._fit_value, self._weight = ru.process_bool_solution(dataset, self._genes)

    def perform_mutation(self):
        valid_mutation = False
        while not valid_mutation:
            #TODO: optimize not to get same randoms
            rnd = random.randint(0, len(self._genes) - 1)
            if self._genes[rnd] == 0:
                if self._weight + dataset["g"][rnd] <= dataset["G"]:
                    self._genes[rnd] = 1
                    self._weight += dataset["g"][rnd]
                    self._fit_value += dataset["v"][rnd]
                    valid_mutation = True
            else:
                self._genes[rnd] = 0
                self._weight -= dataset["g"][rnd]
                self._fit_value -= dataset["v"][rnd]
                valid_mutation = True
        return self

    def mate(self, partner):
        p = random.randint(1, len(self._genes) - 1)
        children = [
            Chromosome(self._genes[:p] + partner._genes[p:]),
            Chromosome(partner._genes[:p] + self._genes[p:])
        ]
        return [child for child in children if child.is_valid()]

    def copy(self):
        return Chromosome(self._genes.copy())

    def __eq__(self, obj):
        return isinstance(obj, Chromosome) and obj._genes == self._genes

class Population:

    def __init__(self, chromosomes, genetic_hyperparameters):
        self._chromosomes = sorted(chromosomes, key=lambda tup:tup.fit_value, reverse=True)
        self._total_value = sum([c.fit_value for c in chromosomes])
        self._no_clonned_chromosomes = round(genetic_hyperparameters["coloning_rate"] * genetic_hyperparameters["population_size"])
        self._no_mutated_chromosomes = round(genetic_hyperparameters["coloning_rate"] * genetic_hyperparameters["population_size"])
        self._no_crossed_chromosomes = genetic_hyperparameters["population_size"] - self._no_clonned_chromosomes - self._no_mutated_chromosomes
    
    @property
    def chromosomes(self):
        return self._chromosomes

    def get_clonned_chromosomes(self):
        return [self._chromosomes[idx] for idx in range(self._no_clonned_chromosomes)]

    def get_random_chromosome(self):
        rand_idx = random.randint(0, len(self._chromosomes) - 1)
        return self._chromosomes[rand_idx]

    def _get_fitted_random_chromosome(self, chromosomes_clone, total_value):
        rand_val = random.randint(0, total_value)
        for idx, chromosome in enumerate(chromosomes_clone):
            rand_val -= chromosome.fit_value
            if rand_val <= 0:
                chromosomes_clone.pop(idx)
                return chromosome   


    def get_fitted_random_chromosome_pair(self):
        tmp_chromosomes = self._chromosomes.copy()      
        c1 = self._get_fitted_random_chromosome(tmp_chromosomes, self._total_value)
        c2 = self._get_fitted_random_chromosome(tmp_chromosomes, self._total_value - c1.fit_value)
        return c1, c2


    def get_mutated_chromosomes(self):
        return [self.get_random_chromosome().copy().perform_mutation() for _ in range(self._no_mutated_chromosomes)]

    def get_crossed_chromosomes(self):
        crossed_chromosomes = []
        crossed_remaining = self._no_crossed_chromosomes
        while crossed_remaining > 0:
            c1, c2 = self.get_fitted_random_chromosome_pair()
            offsprings = c1.mate(c2)
            crossed_chromosomes += offsprings
            crossed_remaining -= len(offsprings)
        return crossed_chromosomes

    def get_next_population_chromosomes(self):
        next_population = self.get_mutated_chromosomes() + self.get_clonned_chromosomes() + self.get_crossed_chromosomes()
        return next_population

    def __str__(self):
        tstr = ""
        prev = None
        cnt = 1;
        for v in self._chromosomes:
            tstr += str(v) + "\n"
        return tstr


def generate_random_population(genetic_hyperparameters):
    return Population([Chromosome(ru.get_random_bool_solution(dataset)) for _ in range(genetic_hyperparameters["population_size"])], genetic_hyperparameters)

def run_genetic_algo(genetic_hyperparameters):
    population_0 = generate_random_population(genetic_hyperparameters)
    print(f"Population_0:\n{population_0}")
    new_population = Population(population_0.get_next_population_chromosomes(), genetic_hyperparameters)
    print(f"Population_1:\n{new_population}")
    no_iterations = genetic_hyperparameters["no_iterations"]
    for _ in range(no_iterations):
        new_population = Population(new_population.get_next_population_chromosomes(), genetic_hyperparameters)
    print(f"Population_{no_iterations+1}:\n{new_population}")
    best_chromosome = new_population.chromosomes[0]
    index_solution = [idx for idx, v in enumerate(best_chromosome.genes) if v == 1]
    value = best_chromosome.fit_value
    return index_solution, value


def main():
    global dataset
    dataset = ru.load_dataset(dataset_name)
    for idx, hp in enumerate(genetic_hyperparameters_arr):
        start = time.time()
        sol, value = run_genetic_algo(hp)
        stop = "%.16f" % (time.time() - start)
        ru.flush_result(sol, value, stop, computation_method, dataset_name + f"_hp_{idx}")
    
if __name__ == '__main__':
    main()