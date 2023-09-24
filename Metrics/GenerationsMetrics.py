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
        avg = self.avg_generations[-1] 
        std = self.std_generations[-1]
        best_fit = self.best_generations[-1]
        return avg, std, best_fit

    def save_statistic(self, data_path, n_iters, execution_num=1, title="Metrics per iteration"):
        self.save_best_avg_statistics(self.best_generations, self.avg_generations, title, execution_num, data_path)
        self.save_avg_std_statistics(self.std_generations, title, execution_num, data_path)
        self.save_avg_execution_metrics(data_path, n_iters)
        plt.close("all") # Close all figures to save RAM

    def save_best_avg_statistics(self, best_indiv_iter, avg_fitness_iter, title, execution_num, data_path):
        plt.figure()
        plt.plot(best_indiv_iter, label= "Best",linestyle='-')
        plt.plot(avg_fitness_iter, label = 'Avg', linestyle='-')
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.grid(True)
        plt.title(title)
        plt.legend()

        path = os.path.join(data_path,f"{title + '_best_avg_' + str(execution_num) }")
        plt.savefig(path)

    def save_avg_std_statistics(self, std_fitness, title, execution_num, data_path):
        plt.figure()
        plt.plot(std_fitness, label= "Std",linestyle='-')
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.grid(True)
        plt.title(title)
        plt.legend()


        path = os.path.join(data_path,f"{title + '_std_' + str(execution_num) }")
        plt.savefig(path)

    def save_avg_execution_metrics(self, data_path, n_iters):
        path = os.path.join(data_path,f"execution_metrics.txt")

        avg, std, best_fit = self.get_execution_metrics()

        with open(path, "w") as file:
            file_txt = f"Avg Fitness {avg} \nStd Fitness {std} \nNum. of iterations {n_iters} \nBest Fitness {best_fit}"
            file.write(file_txt)