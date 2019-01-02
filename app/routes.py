import os
from flask import request, jsonify
from .implementation import Implementation
from app import create_app


red_flags = {}


config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)


@app.route('/')
@app.route('/api/v1')
@app.route('/api/v1')
def home():
    return jsonify({'home': 'welcome to iReporter, please make a request'})


@app.route('/api/v1/red_flags', methods=['POST'])
def create_flag():
    data = request.json
    res = Implementation().create(data)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags', methods=['GET'])
def get_flags():
    res = Implementation().get_flags()
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags/<red_flag_id>', methods=['GET'])
def get_flag(red_flag_id):
    res = Implementation().get_flag(red_flag_id)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags/<red_flag_id>/<key>', methods=['PATCH'])
def edit(red_flag_id, key):
    data = request.json
    res = Implementation().edit(red_flag_id, data, key)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]


@app.route('/api/v1/red_flags/<red_flag_id>', methods=['DELETE'])
def delete_flag(red_flag_id):
    res = Implementation().delete(red_flag_id)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]
