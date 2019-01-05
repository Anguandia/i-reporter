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
def wrongURL(resource, methods=['get'], id=None, action=None):
    if Validation().validateRoute(resource):
        res = Validation().validateRoute(resource)
    elif request.method not in methods:
        res = [405, 'error', 'wrong method']
    return result(res)


@app.route('/api/v1/red_flags', methods=['POST'])
@json_required
def create_flag():
    data = request.json
    return result(Validation().validateNew(data))


@app.route('/api/v1/red_flags', methods=['get'])
def get_flags():
    return result(Implementation().get_flags())


@app.route('/api/v1/red_flags/<red_flag_id>', methods=[
    'get', 'delete'])
def single_flag(red_flag_id):
    if Validation.validateInt(red_flag_id):
        res = [400, 'error', Validation.validateInt(red_flag_id)]
    elif request.method == 'GET':
        res = Implementation().get_flag(red_flag_id)
    elif request.method == 'DELETE':
        res = Implementation().delete(red_flag_id)
    return result(res)


@app.route('/api/v1/red_flags/<red_flag_id>/<key>', methods=[
    'patch'])
@json_required
def edit(red_flag_id, key):
    data = request.json
    res = Validation().validateEdit(data, red_flag_id, key)
    return result(res)


def result(res):
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]
