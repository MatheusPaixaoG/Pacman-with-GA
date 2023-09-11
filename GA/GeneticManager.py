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

    def mutate_weights(self, weight_list):
        weight_list_len = len(weight_list)
        weight_list_idx = random.randrange(weight_list_len)
        weight_list[weight_list_idx] = random.uniform(0.0, 10.0) # Range dos pesos TODO: substituir os valores pelos parâmetros
        return weight_list

    def mutate_dna(self, dna):
        # Mutate normal weights
        normal_weights = dna["normal_weights"]
        normal_weights = self.mutate_weights(normal_weights)
        
        # Mutate powered weigths
        powered_weights = dna["powered_weights"]
        powered_weights = self.mutate_weights(powered_weights)

        # Make new dna
        new_dna = {
            'normal_weights': normal_weights,
            'powered_weights': powered_weights
        }
        return new_dna

    def mutation(self, offspring, prob_of_mutation):
        new_offspring = []
        for individual in offspring:
            num = random.uniform(0.0,1.0)
            if (num <= prob_of_mutation): # Mutate
                dna = copy.deepcopy(individual.dna)
                dna = self.mutate_dna(dna)
                individual.set_dna(dna)
        new_offspring.append(individual)
        
        