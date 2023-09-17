import matplotlib.pyplot as plt
from datetime import datetime
import statistics
import numpy as np
import os

class GenerationsMetrics:

    def __init__(self):
        self.avg_generations = []
        self.std_generations = []
        self.best_generations = []

    def calculate_metrics(self, population_fitness):
        avg = statistics.fmean(population_fitness)
        std = np.std(population_fitness)
        best = max(population_fitness)

        self.avg_generations.append(avg)
        self.std_generations.append(std)
        self.best_generations.append(best)

        return avg, std, best
    
    def get_execution_metrics(self):
        avg_avg = sum(self.avg_generations)/len(self.avg_generations) 
        avg_std = sum(self.std_generations)/len(self.std_generations)
        best_fit = self.best_generations[-1]
        return avg_avg, avg_std, best_fit