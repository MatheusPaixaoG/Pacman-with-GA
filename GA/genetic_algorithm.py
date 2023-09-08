import copy
import random
import sys
sys.path.append("../Pacman_Complete")

# created classes/utils
from Pacman_Complete.constants import *
from params_reader import WEIGHTS_RANGES

class Individual(object):
    def __init__(self, dna, rna):
        self.dna = dna   # dict {'normal_weights': list, 'powered_weights': list}
        self._rna = rna  # dict {'Vector2': list, 'bool': list}

    def genotype(self):
        if not self._rna['bool'][0]:  # powerMode == False
            # Use normal weights
            return [ self._rna['Vector2'][i] * self.dna['normal_weights'][i] for i in range(len(self.dna)) ]
        else:
            # Use power mode weights
            return [ self._rna['Vector2'][i] * self.dna['powered_weights'][i] for i in range(len(self.dna)) ]
    
    def action(self):
        genotype = self.genotype()
        actionVec = sum(genotype)
        return actionVec
        
    def fitness(self):
        return "PONTUAÇÃO FINAL"

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

class PopulationManager:
    def __init__(self):
        self._population = []

    def init_population(self, size):
        return [ Individual(dna=GeneticManager().random_dna_generator()) for _ in range(size) ]
    
    def tournament(self, to_select, n_parents):
        selected = random.sample(self._population,to_select)
        sort_selected = selected.sort(key=lambda x : x.fitness())
        return sort_selected[:n_parents]
    