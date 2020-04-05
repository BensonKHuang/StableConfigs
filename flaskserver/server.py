from stableconfigs import StableConfig
from stableconfigs.common.CustomExceptions import *
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Based expected call/response output of Post to look like Figure 6 from Proj. Definition
@app.route("/", methods=['POST'])
def my_post():
    received_json = request.json
    monomers = received_json['monomers']

    monomer_lines = []
    for index, monomer in enumerate(monomers):
        monomer_lines.append(' '.join(monomer))

    constraints_lines = []
    if 'constraints' in received_json:
        constraints = received_json['constraints']
        for index, token in enumerate(constraints):
            constraints_lines.append((' ').join(token))
    
    gen = 1
    if 'gen' in received_json:
        gen = received_json['gen']

    init_k = 1
    if 'init_k' in received_json:
        init_k = received_json['init_k']

    # Call get stable config and delete file
    config_ouput_list = []
    try:
        config_list, entropy = StableConfig.get_stable_config(monomer_lines, constraints_lines, gen, init_k)
        # Return polymer output in expected format
        for index, config in enumerate(config_list):
            config, config_size = config_to_output(config)
            config_ouput_list.append({
                "polymers": config,
                "polymers_count": config_size
            })

    except TBNException as e:
        print(e)
        response = {
            'success': False,
            'error': {
                'type': type(e).__name__,
                'message': str(e)
            },
        }
        return jsonify(response), 400 

    except Exception as e:
        print(e)
        response = {
            'success': False,
            'error': {
                'type': type(e).__name__,
                'message': str(e)
            },
        }
        return jsonify(response), 401

    else:
        response = {
            'success': True,
            'configs': config_ouput_list,
            'count': len(config_list),
            'entropy': entropy,
        }
        return jsonify(response), 200


def config_to_output(config):
    polymer_output = []
    for index, polymer in enumerate(config):
        cur_polymer = []
        for monomer in polymer.monomer_list:
            cur_monomer = []
            # A BindingSite's name (if it has one) is appended to the end of the site string (a*:name).
            for binding_site in monomer.BindingSites:
                site_str = binding_site.type
                if binding_site.IsComplement:
                    site_str = site_str + "*"
                if binding_site.name is not None:
                    site_str = site_str + ":" + binding_site.name
                cur_monomer.append(site_str)
            # A monomer's name (if it has one) is the last element of the BindingSite list, starting with a '>'.
            if monomer.name is not None:
                cur_monomer.append(">" + monomer.name)
            cur_polymer.append(cur_monomer)
        polymer_output.append(cur_polymer)
    return polymer_output, len(polymer_output)


def run_app():
    app.run(host='0.0.0.0', port=5005)
