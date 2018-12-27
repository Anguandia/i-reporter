from flask import request, jsonify
from .implementation import Implementation
from run import app


@app.route('/')
@app.route('/api/v1')
@app.route('/api/v1/')
def home():
    return jsonify({'home': 'welcome to iReporter, please make a request'})


@app.route('/api/v1/red_flags', methods=['POST'])
def create_flag():
    data = request.json
    res = Implementation().create(data)
    return jsonify({'Status': res[0], res[1]: res[2]}), res[0]
