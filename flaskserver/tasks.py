from stableconfigs import StableConfig
from stableconfigs.common.CustomExceptions import *
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from celery import Celery, states
import json
import os

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.common.TBNProblem import TBNProblem

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

CORS(app)


@celery.task(bind=True)
def compute(self, tbn_lines, constr_lines, gen_count, init_k):

    self.update_state(state="PROGRESS", meta={
                      'status': "Progress", 'count': 0, 'k': 0})

    tbn_problem = parse_input_lines(tbn_lines, constr_lines)
    tbn_problem.gen_count = gen_count
    tbn_problem.init_k = init_k
    sat_problem = SATProblem()

    config_output_list = []
    results, entropy = StableConfig.get_stable_config_v2(self, tbn_problem, sat_problem)

    # Return polymer output in expected format
    for config in results:
        polymers, polymers_count = StableConfig.config_to_output(config)
        config_output_list.append({
            "polymers": polymers,
            "polymers_count": polymers_count
        })

    return {
        'status': "Complete",
        'configs': config_output_list,
        'count': len(results),
        'entropy': entropy
    }

celery.register_task(compute)

@app.route("/task", methods=['POST'])
def create_task():
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
    
    task = compute.apply_async((monomer_lines, constraints_lines, gen, init_k))
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id = task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = compute.AsyncResult(task_id)
    if task.state == "PROGRESS":
        response = {
            'state': task.state,
            'count': task.info.get('count', 1),
            'k': task.info.get('k', 0)
        }

    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'count': task.info.get('count', 0),
            'k': task.info.get('k', 0),
        }

        if 'configs' in task.info:
            response['configs'] = task.info['configs']
        
        if 'entropy' in task.info:
            response['entropy'] = task.info['entropy']

    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


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
            config, config_size = StableConfig.config_to_output(config)
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


def run_app():
    app.run(host='0.0.0.0', port=5005)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
