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
    except:
        response = make_response(jsonify({'message' : 'Error scheculing call to {} @ {}'.format(name, number)}), 500)
    return response

@service_blueprint.route('/callfollowup/<sid>', methods=['POST'])
def call_follow_up(sid):
    answer = request.forms['SpeechResult']
    app.config['callmanager'].call_follow_up(answer, sid)