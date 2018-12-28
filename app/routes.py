import os
from flask import request, jsonify
from .implementation import Implementation
from app import create_app


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
