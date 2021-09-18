from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from twilio.rest import Client
from flask import current_app as app
import os 

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
MY_NUMBER = os.environ['TWILIO_NUMBER']
SERVICE_URL = os.environ['SERVICE_URL']
SECONDS_TO_WAIT = int(os.environ['TIME_TO_WAIT'])   

#
# Encapsulates the Twilio client, being responsible for the state machine.
#
class CubeCallManager():
    def __init__(self):
        self.calls = {}
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("CallManager created")

    #
    # starts the call, passing a twiml which will result (if call answered) on a call
    # to the answer route
    #
    def make_call(self, name, number):
        twiml = """
            <Response>
                <Gather input="dtmf speech" action="{}" timeout="5" hints="no">
                  <Say>Hi {} - This is Alice from Cube Renovation. Thanks for visiting our site today. 
                  We’d love to offer you a first time customer discount in exchange for your honest feedback to a one-question survey. 
                  Since visiting our site, have you purchased a renovation service from another company or pro? 
                  (If No, say “No”, If Yes, say the name of the company you purchased from).</Say>
                </Gather>
            </Response>
        """.format(SERVICE_URL+"/api/answer", name)
        sid = self.client.calls.create(twiml=twiml,
                                       to=number, 
                                       from_=MY_NUMBER)
        print("Calling {} @ {} (sid: {})".format(name, number, sid))

    #
    # checks the response given by the user. must be improved, since answers meaning "no." and "yes." may be given in 
    # many different ways...
    #
    def send_goodbye(self, answer, sid):
        if answer.lower() == 'no.':
            text = """Cube Renovation provides beautiful, architect-designed renovations completed reliably from start to end.
                      We are offering $2,000 off your bath renovation if you stay on the line to speak to a member of our concierge team who can provide you with a free quote."""
        elif answer.lower() == 'yes.':
            text = """We’re sorry to lose your business, and we hope you enjoy your new bathroom."""
        else:
            text = """Thanks for your response. Use code RV20 at checkout to get $500 off if you decide to book with Cube in the future."""
        twiml = "<Response><Say>{}</Say></Response>".format(text)
        self.client.calls(sid).update(twiml=twiml)
        print("Sending goodbye to call {}".format(sid))        

# 
# encapsulates a BackgroundScheduler, delaying each call by an amount of time defined by SECONDS_TO_WAIT.
# should be substituted by a queue manager to improve scalability
#
class CubeScheduler():

    def __init__(self, app):
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.start()
        print("Scheduler created")

    # 
    # this method could make a call to /api/make_call to keep orthogonality, but it'd consume one more http request than needed...
    #
    def schedule_call(self, name, number):
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=SECONDS_TO_WAIT)
        callManager = app.config['callmanager']
        self.scheduler.add_job(lambda: callManager.make_call(name, number), 'date', run_date=now+delta) 
        print("Scheduled call to {} @ {}".format(name, number))