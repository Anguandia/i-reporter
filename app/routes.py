import os
from flask import request, jsonify
from .implementation import Implementation
from app.validation import Validation
from app.wrappers import json_required
from app import create_app


config_name = os.getenv('FLASK_ENV')
app = create_app('TESTING')


@app.route('/')
@app.route('/api/v1')
@app.route('/api/v1/')
def home():
    return jsonify({
      'create or get all flags':
      '/red_flags',
      'get or delete single flag':
      '/red_flags/id',
      'edit flag': '/red_flags/id/field'
      })


@app.route('/api/v1/<resource>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@app.route(
  '/api/v1/<resource>/<id>', methods=['GET', 'POST', 'PATCH', 'DELETE']
  )
@app.route(
  '/api/v1/<resource>/<id>/<action>',
  methods=['GET', 'POST', 'PATCH', 'DELETE']
  )
def wrongURL(resource, id=None, action=None):
    if resource != 'red_flags':
        return jsonify(
            {'Status': 400, 'error': f'wrong url, check \'{resource}\''}
            ), 400


@app.route('/api/v1/red_flags', methods=['POST'])
@json_required
def create_flag():
    if request.method != 'POST':
        res = [405, 'error', 'wrong method']
    else:
        data = request.json
        res = Validation().validateNew(data)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags', methods=['get', 'post', 'patch', 'delete'])
def get_flags():
    if request.method != 'GET':
        res = [405, 'error', 'wrong method']
    else:
        res = Implementation().get_flags()
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags/<red_flag_id>', methods=[
    'get', 'delete', 'post', 'patch'])
def single_flag(red_flag_id):
    if Validation.validateId(red_flag_id):
        res = [400, 'error', Validation.validateId(red_flag_id)]
    elif request.method == 'GET':
        res = Implementation().get_flag(red_flag_id)
    elif request.method == 'DELETE':
        res = Implementation().delete(red_flag_id)
    else:
        res = [405, 'error', 'wrong method']
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags/<red_flag_id>/<key>', methods=[
    'patch', 'get', 'delete', 'post'])
@json_required
def edit(red_flag_id, key):
    if request.method != 'PATCH':
        res = [405, 'error', 'wrong method']
    else:
        data = request.json
        res = Validation().validateEdit(data, red_flag_id, key)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]
