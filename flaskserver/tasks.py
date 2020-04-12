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
Celery.register_task
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
    StableConfig.get_stable_config_v2(self, tbn_problem, sat_problem)

    # Return polymer output in expected format
    for config in tbn_problem.results:
        config, config_size = config_to_output(config)
        config_output_list.append({
            "polymers": config,
            "polymers_count": config_size
        })

    return{
        'status': "Complete",
        'configs': config_output_list,
        'count': len(tbn_problem.results),
        'entropy': tbn_problem.original_num_reps
    }


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
