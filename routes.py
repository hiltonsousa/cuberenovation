from flask import Blueprint, json, jsonify, request, make_response
from werkzeug.wrappers import response 
from flask import current_app as app

cube_blueprint = Blueprint('cube', __name__, url_prefix="/api")

@cube_blueprint.route('/callme', methods=['POST'])
def schedule_call():
    number = request.form['number']
    name = request.form['name']
    try:
        app.config['scheduler'].schedule_call(name, number)
        response = make_response(jsonify({'message' : 'Scheduled call to {} @ {}'.format(name, number)}), 200)
    except:
        response = make_response(jsonify({'message' : 'Error scheculing call to {} @ {}'.format(name, number)}), 500)
    return response

