import os
from flask import request, jsonify
from .implementation import Implementation
from app.validation import Validation
from app.wrappers import json_required
from app import create_app


red_flags = {}


config_name = os.getenv('FLASK_ENV')
app = create_app('TESTING')


@app.route('/')
@app.route('/api/v1')
@app.route('/api/v1/')
def home():
    return jsonify({'home': 'welcome to iReporter, please make a request'})


@app.route('/api/v1/<resource>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@app.route(
  '/api/v1/<resource>/<id>', methods=['GET', 'POST', 'PATCH', 'DELETE']
  )
@app.route(
  '/api/v1/<resource>/<id>/<action>',
  methods=['GET', 'POST', 'PATCH', 'DELETE']
  )
def wrongEndpoint(resource, id=None, action=None):
    if resource != 'red_flags':
        resp = [400, f'wrong url, error in spelling of \'{resource}\'']
    elif id and not action:
        if request.method == 'POST':
            resp = [
              405, f'red-flag id\'s are generated automatically,\
              remove \'{id}\'']
        elif request.method == 'PATCH':
            resp = [405, 'wrong method or specify field to edit in url']
    elif id and action:
        if action not in ['location', 'status', 'comment']:
            resp = [400, f'wrong endpoint, verify \'{action}\'']
        elif request.method != 'PATCH':
            resp = [405, f'wrong method, tis url is for editing {action}']
    else:
        if request.method not in ['POST', 'GET']:
            resp = [405, 'wrong method']
    return jsonify({'Status': resp[0], 'error': resp[1]}), resp[0]


@app.route('/api/v1/red_flags', methods=['POST'])
@json_required
def create_flag():
    data = request.json
    res = Validation().validateNew(data)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags', methods=['GET'])
def get_flags():
    res = Implementation().get_flags()
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags/<red_flag_id>', methods=['GET', 'DELETE'])
def single_flag(red_flag_id):
    if Validation.validateId(red_flag_id):
        res = [400, 'error', Validation.validateId(red_flag_id)]
    elif request.method == 'GET':
        res = Implementation().get_flag(red_flag_id)
    else:
        res = Implementation().delete(red_flag_id)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags/<red_flag_id>/<key>', methods=['PATCH'])
@json_required
def edit(red_flag_id, key):
    data = request.json
    res = Validation().validateEdit(data, red_flag_id, key)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]
