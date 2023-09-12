import random, sys
sys.path.append("../")

from GA.Individual import Individual
from GA.GeneticManager import GeneticManager

class PopulationManager:
    def __init__(self, size):
        self._size = size
        self._population = []

    def init_population(self):
        self._population = [ Individual(dna=GeneticManager().random_dna_generator()) for _ in range(self._size) ]
    
    def tournament(self, to_select, n_parents):
        selected = random.sample(self._population,to_select)
        sort_selected = selected.sort(key=lambda x : x.fitness())
        return sort_selected[:n_parents]
    
    def survival_elitist(self, offspring):
        new_population = self._population + offspring
        sort_new_pop = new_population.sort(key=lambda x : x.fitness())
        self._population = sort_new_pop[:self._size]
    
    def survival_replace(self, parents, offspring):
        n_parents = len(parents)
        best_offspring = offspring.sort(key=lambda x : x.fitness())[:n_parents]
        for parent in range(n_parents):
            self._population.remove(parents[parent])
            self._population.append(best_offspring)
    
    def get_population(self):
        return self._population