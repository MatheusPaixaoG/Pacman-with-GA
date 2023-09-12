import json

CROSSOVER = {}
POPULATION = {}
RUN = {}
WEIGHTS_RANGES = {}

def load_params():
    global CROSSOVER, POPULATION, RUN, WEIGHTS_RANGES
    params_path = "./params.json"
    with open(params_path) as f:
        params = json.load(f)

        WEIGHTS_RANGES.update({'normal_weights':params['normal_weights']})
        WEIGHTS_RANGES.update({'powered_weights':params['powered_weights']})

        POPULATION = params['population']
        CROSSOVER = params['crossover']
        RUN = params['run']
    f.close()