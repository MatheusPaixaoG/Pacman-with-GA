import json

WEIGHTS = {}

params_path = input("PATH of the params file: ")

with open(params_path) as f:
    params = json.load(f)
    WEIGHTS = params['weight_ranges'][0]