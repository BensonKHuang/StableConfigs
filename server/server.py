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
        my_file = "temp.txt"
        f = open(my_file, "w+")
        for index, monomer in enumerate(monomers):
            f.write(' '.join(monomer))
            if index != len(monomers) - 1:
                f.write('\n')
        f.close()

        # Call get stable config and delete file
        polymers = StableConfig.get_stable_config(my_file)
        os.remove(my_file)

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
