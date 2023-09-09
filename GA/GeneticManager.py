import copy, random

from params_reader import WEIGHTS_RANGES

class GeneticManager:

    def random_dna_generator(self):
        return {
            'normal_weights': [random.uniform(i[0],i[1]) for i in WEIGHTS_RANGES['normal_weights'].values()],
            'powered_weights': [random.uniform(i[0],i[1]) for i in WEIGHTS_RANGES['powered_weights'].values()]
        }
    
    def crossover(self, parents, offspring_size=1, splits=0):
        offspring = []
        
        for o in range(offspring_size):
            base_parent = parents[o % len(parents)]
            child = copy.deepcopy(base_parent)
            offspring.append(child)
        
        