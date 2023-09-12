class Individual(object):
    def __init__(self, dna):
        self.dna = dna   # dict {'normal_weights': list, 'powered_weights': list}
        self.fitness = None

    def genotype(self, rna):
        # rna == dict {'Vector2': list, 'bool': list}
        if not rna['bool'][0]:  # powerMode == False
            # Use normal weights
            return [ rna['Vector2'][i] * self.dna['normal_weights'][i] for i in range(len(self.dna)) ]
        else:
            # Use power mode weights
            return [ rna['Vector2'][i] * self.dna['powered_weights'][i] for i in range(len(self.dna)) ]

    def set_dna(self, dna):
        self.dna = dna

    def get_action(self, rna):
        genotype = self.genotype(rna)
        actionVec = genotype[0]
        for i in range(1,len(genotype)):
            actionVec += genotype[i]
        return actionVec
        
    def set_fitness(self, fitness):
        self.fitness = fitness
    
    def get_fitness(self):
        return self.fitness
