# Pacman-with-GA 👻

Code from Pacman available at https://pacmancode.com/

# Parameters:

## _weights:_
    The possible range for random initialization of DNA weights.
        [a,b] -> a,b are positive floats.
## _crossover:_
### - _prob_of_crossover_
    Chance of crossover occurring. 
        n -> float between (and including) 0 and 1.
### - _alpha_
    Alpha for arithmetic combination crossover. Only used when 2 parents are selected for crossover.
        α -> float between (and including) 0 and 1. Choosing 0 means that only the genes from the second parent will be chosen and 1 the opposite.
### - _offspring_size_
    Size of the generated offspring.
        n -> positive int (must be less or equal the population size).
### - _type_
    The crossover type.
        "simple": replaces only one gene.
        "normal": randomly selects a gene at the k position, and replaces k+1 until the final gene.
        "complete": replaces the entire DNA.
## _mutation:_
### - _prob_of_mutation_
    Chance of mutation occurring. 
        n -> float between (and including) 0 and 1.
## _population:_
### - _size_
    Population's size. 
        n -> positive int.
### - _tournament_to_select_
    The selected individuals from the population to participate into tournament.
        n -> positive int (must be less than the population size).
### - _tournament_n_parents_
    The number of parents selected from the tournament.
        n -> positive int.
### - _survival_
    The survival selection type.
        "elitist": merges the offspring with the population and selects only the best.
        "replace": replaces the parents with the offspring.
## _run:_
### - _iterations_
    The number of generations to be created. 
        n -> positive int.
### - _early_stopping_max_iters_
    Early stopping's maximum number of iterations to check if the score doesn't increase.
        n -> positive int (must be less than the number of generations).
## _individual:_
    Recreate and run a individual.
        [normal],[power] -> the individual's dna.

# How to run
This code uses [Python](https://www.python.org/) 3.10 or newer. 

## Install dependencies
We recommend you to create a virtual environment for running the studies.
On the local repository's root path:
```
pip install -r requirements.txt
```
## Study's parameters path
Configure the parameters on:
_Pacman_Complete/params.json_

## Running the study
Go to "Pacman_Complete" and run:
```
python run.py
```
The PyGame window will appear with the study running and the log will be on the console.
Also, an "data" folder containing further study data will appear on the "Pacman_Complete" path with the folder named with the datetime that the study started.
