import copy, random


class Mutation:

    def __mutate_weights(self, weight_list):
        weight_list_len = len(weight_list)
        weight_list_idx = random.randrange(weight_list_len)
        weight_list[weight_list_idx] = random.uniform(0.0, 10.0) # Range dos pesos TODO: substituir os valores pelos parâmetros
        return weight_list

    def __mutate_dna(self, dna):
        # Mutate normal weights
        normal_weights = dna["normal_weights"]
        normal_weights = self.__mutate_weights(normal_weights)
        
        # Mutate powered weigths
        powered_weights = dna["powered_weights"]
        powered_weights = self.__mutate_weights(powered_weights)

        # Make new dna
        new_dna = {
            'normal_weights': normal_weights,
            'powered_weights': powered_weights
        }
        return new_dna

    def mutate(self, offspring, prob_of_mutation):
        new_offspring = []
        for individual in offspring:
            num = random.uniform(0.0,1.0)
            if (num <= prob_of_mutation): # Mutate
                dna = copy.deepcopy(individual.dna)
                dna = self.__mutate_dna(dna)
                individual.set_dna(dna)
            new_offspring.append(individual)
        return new_offspring

