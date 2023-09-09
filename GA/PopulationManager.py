import random

import Individual, GeneticManager

class PopulationManager:
    def __init__(self):
        self._population = []

    def init_population(self, size):
        return [ Individual(dna=GeneticManager().random_dna_generator()) for _ in range(size) ]
    
    def tournament(self, to_select, n_parents):
        selected = random.sample(self._population,to_select)
        sort_selected = selected.sort(key=lambda x : x.fitness())
        return sort_selected[:n_parents]
    