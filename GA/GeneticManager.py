import copy, random, sys
sys.path.append("../")

from GA.Crossover import Crossover
from GA.Mutation import Mutation
from Pacman_Complete.params_reader import CROSSOVER, N_WEIGHTS, WEIGHTS_RANGES

class GeneticManager:

    def random_dna_generator(self):
        return {
            'normal_weights': [random.uniform(WEIGHTS_RANGES[0],WEIGHTS_RANGES[1]) for _ in range(N_WEIGHTS)],
            'powered_weights': [random.uniform(WEIGHTS_RANGES[0],WEIGHTS_RANGES[1]) for _ in range(N_WEIGHTS)]
        }
    
    def crossover(self, parents):
        if random.uniform(0.0,1.0) > CROSSOVER['prob_of_crossover']:
            return [copy.deepcopy(parents[i%len(parents)]) for i in range(CROSSOVER['offspring_size'])]
        if (CROSSOVER["type"] == "simple"):
            return Crossover().simple_crossover(parents)
        elif (CROSSOVER["type"] == "normal"):
            return Crossover().normal_crossover(parents)
        elif (CROSSOVER["type"] == "complete"):
            return Crossover().complete_crossover(parents)
        else:
            print("This crossover type does not exist or was not implemented.")

    def mutation(self, offspring):
        return Mutation().mutate(offspring)
