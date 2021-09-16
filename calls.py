from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from twilio.rest import Client
from flask import current_app as app

TWILIO_ACCOUNT_SID = 'AC37b0224ede54804a1b1a597e2fa208d0'
TWILIO_AUTH_TOKEN = 'e28f18fec5ebee7833d782dbfefe4393'
MY_NUMBER = '+15707052076'
SERVICE_URL = "https://cuberenovation.herokuapp.com"
#SERVICE_URL = "https://7642-2804-14c-5bb3-a19a-410f-b5a1-7736-5d5.ngrok.io"
SECONDS_TO_WAIT = 5   

class CubeCallManager():
    def __init__(self):
        self.calls = {}
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("CallManager created")

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

class CubeScheduler():

    def __init__(self, app):
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.start()
        print("Scheduler created")

    def schedule_call(self, name, number):
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=SECONDS_TO_WAIT)
        callManager = app.config['callmanager']
        self.scheduler.add_job(lambda: callManager.make_call(name, number), 'date', run_date=now+delta) 
        print("Scheduled call to {} @ {}".format(name, number))