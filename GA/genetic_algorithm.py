import copy
import random
import sys
sys.path.append("../Useful_information")

# created classes/utils
from params_reader import WEIGHTS

class Individual(object):
    def __init__(self, dna, rna):
        self.dna = dna
        self._rna = rna  # dict {'Vector2': list, 'bool': list}

    def genotype(self):
        rna_vector2 = [ self._rna['Vector2'][i] * self.dna[i] for i in range(len(self.dna)) ]
        return rna_vector2 # + self._rna['bool']
    
    def fitness(self):
        return "PONTUAÇÃO FINAL"

class GeneticManager:

    def random_dna_generator(self):
        return [random.uniform(i[0],i[1]) for i in WEIGHTS.values()]
    
    def crossover(self, parents, offspring_size=1, splits=0):
        offspring = []
        
        for o in range(offspring_size):
            base_parent = parents[o % len(parents)]
            child = copy.deepcopy(base_parent)
            offspring.append(child)
