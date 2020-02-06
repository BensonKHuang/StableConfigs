from stableconfigs import StableConfig
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Based expected call/response output of Post to look like Figure 6 from Proj. Definition
@app.route("/", methods=['POST'])
def my_post():
        received_json = request.get_json()
        monomers = received_json['monomers']

        # Creates a file to write monomers in order to call get_stable_config
        monomer_file_path = "temp.txt"
        monomer_f = open(monomer_file_path, "w+")
        for index, monomer in enumerate(monomers):
            monomer_f.write(' '.join(monomer))
            if index != len(monomers) - 1:
                monomer_f.write('\n')
        monomer_f.close()

        instructions = received_json['instructions']
        instr_file_path = "instr.txt"
        instr_f = open(instr_file_path, "w+")
        for index, token in enumerate(instructions):
            instr_f.write(' '.join(token))
            if index != len(instructions) - 1:
                instr_f.write('\n')
        instr_f.close()

        # Call get stable config and delete file
        polymers = StableConfig.get_stable_config(monomer_file_path, instr_file_path)
        os.remove(monomer_file_path)
        os.remove(instr_file_path)

        # Return polymer output in expected format
        polymer_output = []
        polymer_count = len(polymers)
        for index, polymer in enumerate(polymers):
            cur_polymer = []
            for monomer in polymer.monomer_list:
                cur_monomer = list(map(lambda x: (x.name + "*") if x.IsComplement else x.name, monomer.BindingSites))
                cur_polymer.append(cur_monomer)
            polymer_output.append(cur_polymer)

        return jsonify({"polymers": polymer_output}, {"polymers count": polymer_count}), 201


def run_app():
    app.run(debug=False, use_reloader=False, threaded=False)
