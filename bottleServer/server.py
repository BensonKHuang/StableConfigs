from stableconfigs import StableConfig
from bottle import post, run, request, Bottle, HTTPResponse
import json
import os

app = Bottle()

# Based expected call/response output of Post to look like Figure 6 from Proj. Definition
@app.post("/")
def my_post():
        received_json = request.json
        monomers = received_json['monomers']

        monomer_lines = []
        for index, monomer in enumerate(monomers):
            monomer_lines.append(' '.join(monomer))

        
        instr_lines = []
        if 'instructions' in received_json:
            instructions = received_json['instructions']
            for index, token in enumerate(instructions):
                instr_lines.append((' ').join(token))
        
        gen = 1
        if 'gen' in received_json:
            gen = received_json['gen']

        # Call get stable config and delete file
        succ, config_list = StableConfig.get_stable_config(monomer_lines, instr_lines, gen)
        if not succ:
            return HTTPResponse(status=403, body='Something went wrong')

        # Return polymer output in expected for mat
        config_ouput_list = []
        for index, config in enumerate(config_list):
            config, config_size = config_to_output(config)
            config_ouput_list.append({
                "polymers": config, 
                "polymers_count": config_size
            })

        return json.dumps({"configs":config_ouput_list})

def config_to_output(config):
    polymer_output = []
    for index, polymer in enumerate(config):
        cur_polymer = []
        for monomer in polymer.monomer_list:
            cur_monomer = list(map(lambda x: (x.type + "*") if x.IsComplement else x.type, monomer.BindingSites))
            cur_polymer.append(cur_monomer)
        polymer_output.append(cur_polymer)
    return polymer_output, len(polymer_output)


def run_app():
    run(app, host='0.0.0.0', port=5005)
