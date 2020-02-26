from stableconfigs import StableConfig
from bottle import post, run, request, Bottle
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

        # Call get stable config and delete file
        succ, polymers = StableConfig.get_stable_config(monomer_lines, instr_lines, 1)

        if not succ:
            return polymers  # TODO: replace with JSON error message right here, the 'polymers' variable has the msg

        # Return polymer output in expected format
        polymer_output = []
        polymer_count = len(polymers)
        for index, polymer in enumerate(polymers):
            cur_polymer = []
            for monomer in polymer.monomer_list:
                cur_monomer = list(map(lambda x: (x.type + "*") if x.IsComplement else x.type, monomer.BindingSites))
                cur_polymer.append(cur_monomer)
            polymer_output.append(cur_polymer)

        return json.dumps({"polymers": polymer_output, "polymers_count": polymer_count})


def run_app():
    run(app, host='0.0.0.0', port=5005)
