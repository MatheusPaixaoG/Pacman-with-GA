import json

CROSSOVER = {}
MUTATION = {}
POPULATION = {}
RUN = {}
WEIGHTS_RANGES = {}

def load_params():
    global CROSSOVER, MUTATION, POPULATION, RUN, WEIGHTS_RANGES
    params_path = "./params.json"
    with open(params_path) as f:
        params = json.load(f)

        WEIGHTS_RANGES.update({'normal_weights':params['normal_weights']})
        WEIGHTS_RANGES.update({'powered_weights':params['powered_weights']})

        CROSSOVER = params['crossover']
        MUTATION = params['mutation']
        POPULATION = params['population']
        RUN = params['run']
    f.close()

load_params()