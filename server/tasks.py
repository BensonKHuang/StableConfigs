from __future__ import absolute_import, unicode_literals
from stableconfigs import StableConfig
from stableconfigs.common.CustomExceptions import *
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from celery import Celery, states
from celery.exceptions import SoftTimeLimitExceeded, Ignore
from celery.app.control import Control
from celery.contrib.abortable import AbortableTask

import json
import os

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.common.TBNProblem import TBNProblem

app = Flask(__name__)
CORS(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL']
)

# Configure timeout of redis broker cache to 5 minutes
celery.conf.update(app.config)
celery.conf.result_expires = 300

# Celery Tasks
@celery.task(name='tasks.compute', bind=True, time_limit=240, soft_time_limit=120, base=AbortableTask)
def compute(self, tbn_lines, constr_lines, gen_count, init_k):

    self.update_state(state="PROGRESS", meta={'status': "Progress", 'count': 0, 'k': 0})

    config_output_list = []
    try:
        results, entropy = StableConfig.get_stable_config(
            tbn_lines, constr_lines, gen_count, init_k, self)
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

    except Exception as e:
        # Exceptions will automatically fail the task
        print("Exception occurred: " + str(e))


# API Routes
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
    
    task = compute.apply_async(
        (monomer_lines, constraints_lines, gen, init_k))
    response = {'task_id': task.id}
    return jsonify(response), 202


@app.route('/status/<task_id>', methods=['GET'])
def taskstatus(task_id):
    task = compute.AsyncResult(task_id)
    
    # Complete
    if task.ready() and task.result is not None:
        response = {
            'state': task.state,
            'configs': task.result["configs"],
            'count': task.result["count"],
            'entropy': task.result["entropy"]
        }
        return jsonify(response), 200

    # Timeout
    elif task.ready() and task.result is None:
        # Timeout occurred
        response = {
            'status': "Timed out exception"  # this is the exception raised
        }
        return jsonify(response), 401

    # In Progress
    elif task.state == "PROGRESS":
        response = {
            'status': task.info.get('status', "Unavailable"),
            'count': task.info.get('count', 1),
            'k': task.info.get('k', 0),
        }
        return jsonify(response), 202

    # Input Failure
    elif task.state == states.FAILURE:
        response = {
            'status': str(task.info)  # this is the exception raised
        }
        return jsonify(response), 400

    # Unexpected Case
    else:
        # something went wrong in the background job
        response = {
            'status': str(task.info),  # this is the exception raised
        }
        return jsonify(response), 402


@app.route('/terminate/<task_id>', methods=['DELETE'])
def terminate_task(task_id):
    task = compute.AsyncResult(task_id)
    task.abort()
    response = {
        'status': 'terminating task: ' + str(task_id)
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
