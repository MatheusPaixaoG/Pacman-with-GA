class Individual(object):
    def __init__(self, dna, rna):
        self.dna = dna
        self._rna = rna  # dict {'Vector2': list, 'bool': list}

    def genotype(self):
        rna_vector2 = [ self._rna['Vector2'][i] * self.dna[i] for i in range(len(self.dna)) ]
        return rna_vector2 # + self._rna['bool']
    
    def fitness(self):
        return "PONTUAÇÃO FINAL"
