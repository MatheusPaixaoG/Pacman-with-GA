import json

WEIGHTS_RANGES = {}

params_path = input("PATH of the params file: ")

with open(params_path) as f:
    params = json.load(f)
    WEIGHTS_RANGES.update({'normal_weights':params['normal_weights']})
    WEIGHTS_RANGES.update({'powered_weights':params['powered_weights']})