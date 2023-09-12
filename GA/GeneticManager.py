import random, sys
sys.path.append("../")

from GA.Crossover import Crossover
from GA.Mutation import Mutation
from Pacman_Complete.params_reader import CROSSOVER, WEIGHTS_RANGES

class GeneticManager:

    def random_dna_generator(self):
        return {
            'normal_weights': [random.uniform(i[0],i[1]) for i in WEIGHTS_RANGES['normal_weights'].values()],
            'powered_weights': [random.uniform(i[0],i[1]) for i in WEIGHTS_RANGES['powered_weights'].values()]
        }
    
    def crossover(self, parents):
        if (CROSSOVER["type"] == "simple"):
            return Crossover().simple_crossover(parents)
        elif (CROSSOVER["type"] == "normal"):
            return Crossover().normal_crossover(parents)
        elif (CROSSOVER["type"] == "complete"):
            return Crossover().complete_crossover(parents)
        else:
            print("This crossover type does not exist or was not implemented.")

    def mutation(self, offspring, prob_of_mutation):
        return Mutation().mutate(offspring, prob_of_mutation)
