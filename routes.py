from flask import Blueprint, json, jsonify, request, make_response, render_template

from werkzeug.wrappers import response 
from flask import current_app as app
from twilio.twiml.voice_response import Gather, VoiceResponse, Say

service_blueprint = Blueprint('service', __name__, url_prefix="/api")
ui_blueprint = Blueprint('ui', __name__, url_prefix="/")

@ui_blueprint.route("", methods=['GET'])
def main_page():
    return render_template('index.html')

@service_blueprint.route('/callme', methods=['POST'])
def call_me():
    number = request.form['number']
    name = request.form['name']
    try:
        app.config['scheduler'].schedule_call(name, number)
        response = make_response(jsonify({'message' : 'Scheduled call to {} @ {}'.format(name, number)}), 200)
    except Exception as e:
        print(e)
        response = make_response(jsonify({'message' : 'Error scheculing call to {} @ {}'.format(name, number)}), 500)
    return response

@service_blueprint.route('/makecall', methods=['POST'])
def make_call():
    name = request.form['name']
    number = request.form['number']
    app.config['callmanager'].make_call(name, number)
    return make_response(jsonify({'message' : 'Making call'}), 200)

@service_blueprint.route('/answer', methods=['POST'])
def answer():
    answer = request.form['SpeechResult']
    sid = request.form['CallSid']
    print("Answer: {}".format(answer))
    app.config['callmanager'].send_goodbye(answer, sid)
    return make_response(jsonify({'message' : 'User has answered'}), 200)