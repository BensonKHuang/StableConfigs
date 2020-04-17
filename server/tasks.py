from __future__ import absolute_import, unicode_literals
from stableconfigs import StableConfig
from stableconfigs.common.CustomExceptions import *
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from celery import Celery, states
from celery.exceptions import SoftTimeLimitExceeded, Ignore
from celery.app.control import Control
from celery.contrib.abortable import AbortableTask

import collections
import json
import os

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.common.TBNProblem import TBNProblem

TIMEOUT = 90

app = Flask(__name__)
CORS(app)

# Celery configuration
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'
celery = Celery(
    app.name,
    broker=app.config['broker_url']
)

celery.conf.update(app.config)

# Celery results only exist in Redis backend results for 5 minutes
celery.conf.result_expires = 300
# Celery workers will restart after 20 tasks are run
celery.conf.worker_max_tasks_per_child = 20
# Celery workers will restart after exceeding 150 MB (150,000 KB) of resident memory (will complete the task still)
celery.conf.worker_max_memory_per_child = 150000

# Celery Task, Raises timeout exception after 90 seconds (configurable, but soft_time_limit < time_limit)
@celery.task(name='tasks.compute', bind=True, time_limit=TIMEOUT*2, soft_time_limit=TIMEOUT, base=AbortableTask)
def compute(self, tbn_lines, constr_lines, gen_count, init_k):

    self.update_state(state="PROGRESS", meta={'status': "Progress", 'count': 0, 'k': 0})

    config_output_list = []
    response = ""
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

    except SoftTimeLimitExceeded as e:
        response = {
            'status': "Timeout",
            'message': str(e)
        }

    except TBNException as e:
        response = {
            'status': "TBNException",
            'message': str(e)
        }
    # Unexpected Exception
    except Exception as e:
        response = {
            'status': "Exception",
            'message': str(e)
        }
    # Succeed
    else:
        response = {
            'status': "Completed",
            'configs': config_output_list,
            'count': len(results),
            'entropy': entropy
        }

    return response

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
    if task.ready() or task.state == states.SUCCESS:
        # Unexpected exception / Empty result / Server error
        if task.result is None or isinstance(task.result, Exception):
            response = jsonify(task.result)
            task.forget()
            return response, 402

        # Succeed
        elif task.result["status"] == "Completed":
            return jsonify(task.result), 200

        # Timeout
        elif task.result["status"] == "Timeout":
            return jsonify(task.result), 400

        # TBN Exception
        elif task.result["status"] == "TBNException":
            return jsonify(task.result), 401

        # All catch, default to Exception
        else:
            return jsonify(task.result), 402

    # In Progress
    elif task.state == "PROGRESS" or task.state == states.PENDING:
        return jsonify(task.info), 202

    else:
        # There is a race issue, where the results available right after calling task.ready().
        # Return a 203 to signal user to try again (!!!)
        return jsonify("Please GET /status of task again."), 203



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
