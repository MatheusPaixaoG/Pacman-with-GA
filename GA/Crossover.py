import copy, random

import Individual
from params_reader import WEIGHTS_RANGES, CROSSOVER

class BaseCrossover(object):
    
    def __discrete_choice(parents, gene_idx):
        parent = random.choice(parents)
        normal_gene = parent.dna['normal_weights'][gene_idx]
        powered_gene = parent.dna['powered_weights'][gene_idx]
        return normal_gene, powered_gene

    def __aritimetic_combination(parent1, parent2, gene_idx):
        normal_gene = CROSSOVER["alpha"] * parent1.dna['normal_weights'][gene_idx] + (1 - CROSSOVER["alpha"]) * parent2.dna['normal_weights'][gene_idx]
        powered_gene = CROSSOVER["alpha"] * parent1.dna['powered_weights'][gene_idx] + (1 - CROSSOVER["alpha"]) * parent2.dna['powered_weights'][gene_idx]
        return normal_gene, powered_gene

    def __base_crossover(self, parents, cut_point, quant_to_modify, offspring_idx):
        num_parents = len(parents)
        offspring_dna = copy.deepcopy(parents[offspring_idx % num_parents].dna)

        if (num_parents < 2):
            print("At least 2 parents needed!")
            return
        elif (num_parents == 2):
            
            for q in range(quant_to_modify):
                normal_gene, powered_gene = self.__aritimetic_combination(parents[0],parents[1],cut_point + q)
                if (offspring_idx % 2 == 0):
                    normal_gene, powered_gene = self.__aritimetic_combination(parents[1],parents[0],cut_point + q)
                offspring_dna['normal_weights'][cut_point + q] = normal_gene
                offspring_dna['powered_weights'][cut_point + q] = powered_gene
                    
        else: #num_parents > 2
            
            for q in range(quant_to_modify):
                normal_gene, powered_gene = self.__discrete_choice(parents,cut_point + q)
                offspring_dna['normal_weights'][cut_point + q] = normal_gene
                offspring_dna['powered_weights'][cut_point + q] = powered_gene
            
        return offspring_dna
    
    def simple_crossover(self, parents):
        offspring = []
        quant_to_modify = 1
        num_children = CROSSOVER["offspring_size"]

        for i in range(num_children):
            cut_point = random.randint(0,len(list(WEIGHTS_RANGES["normal_weights"].values()))-1)

            new_individual_dna = self.__base_crossover(parents, cut_point, quant_to_modify, i)
            offspring.append( Individual(new_individual_dna) )

        return offspring
    
    def normal_crossover(self, parents):
        offspring = []
        num_children = CROSSOVER["offspring_size"]

        for i in range(num_children):
            cut_point = random.randint(0,len(list(WEIGHTS_RANGES["normal_weights"].values()))-1) + 1
            quant_to_modify = len(parents[0].gene) - cut_point

            new_individual_dna = self.__base_crossover(parents, cut_point, quant_to_modify, i)
            offspring.append( Individual(new_individual_dna) )
            
        return offspring

    def complete_crossover(self, parents):
        offspring = []
        quant_to_modify = len(parents[0].gene)
        cut_point = 0
        num_children = CROSSOVER["offspring_size"]

        for i in range(num_children):
            new_individual_dna = self.__base_crossover(parents, cut_point, quant_to_modify, i)
            offspring.append( Individual(new_individual_dna) )

        return offspring