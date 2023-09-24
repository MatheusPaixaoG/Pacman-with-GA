import random, sys
sys.path.append("../")

from GA.GeneticManager import GeneticManager
from GA.Individual import Individual
from Pacman_Complete.params_reader import POPULATION

class PopulationManager:
    def __init__(self):
        self._population = []

    def init_population(self):
        self._population = [ Individual(dna=GeneticManager().random_dna_generator()) for _ in range(POPULATION['size']) ]

    def tournament(self):
        selected = random.sample(self._population,POPULATION['tournament_to_select'])
        sort_selected = sorted(selected,key=lambda x : x.get_fitness(), reverse=True)
        return sort_selected[:POPULATION['tournament_n_parents']]
    
    def survival_elitist(self, offspring):
        new_population = self._population + offspring
        sort_new_pop = sorted(new_population,key=lambda x : x.get_fitness(), reverse=True)
        self._population = sort_new_pop[:POPULATION['size']]
    
    def survival_replace(self, parents, offspring):
        #TODO: fix replacement
        n_parents = len(parents)
        best_offspring = sorted(offspring,key=lambda x : x.get_fitness(), reverse=True)[:n_parents]
        for parent in range(n_parents):
            self._population.remove(parents[parent])
            self._population.append(best_offspring)
    
    def get_population(self):
        return self._population