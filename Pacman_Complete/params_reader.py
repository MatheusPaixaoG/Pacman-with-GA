import json

CROSSOVER = {}
MUTATION = {}
POPULATION = {}
RUN = {}
WEIGHTS_RANGES = []

N_WEIGHTS = 4

params_path = "./params.json"
with open(params_path) as f:
    params = json.load(f)

    CROSSOVER = params['crossover']
    MUTATION = params['mutation']
    POPULATION = params['population']
    RUN = params['run']
    WEIGHTS_RANGES = params['weights']
    
    f.close()
