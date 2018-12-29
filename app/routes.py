import os
from flask import request, jsonify
from app import create_app


red_flags = {}


config_name = os.getenv('FLASK_ENV')
app = create_app('TESTING')


@app.route('/')
@app.route('/api/v1')
@app.route('/api/v1/')
def home():
    return jsonify({'home': 'welcome to iReporter, please make a request'})
