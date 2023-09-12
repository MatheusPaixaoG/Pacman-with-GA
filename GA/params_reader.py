import json

WEIGHTS_RANGES = {}
CROSSOVER = {}
RUN = {}

def load_params():
    global WEIGHTS_RANGES, CROSSOVER, RUN
    params_path = "params.json"
    with open(params_path) as f:
        params = json.load(f)

        WEIGHTS_RANGES.update({'normal_weights':params['normal_weights']})
        WEIGHTS_RANGES.update({'powered_weights':params['powered_weights']})

        
        CROSSOVER = params['crossover']
        RUN = params['run']