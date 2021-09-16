from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from twilio.rest import Client
from flask import current_app as app

TWILIO_ACCOUNT_SID = 'AC37b0224ede54804a1b1a597e2fa208d0'
TWILIO_AUTH_TOKEN = 'e28f18fec5ebee7833d782dbfefe4393'
MY_NUMBER = '+15707052076'
SERVICE_URL = "https://cuberenovation.herokuapp.com"
SECONDS_TO_WAIT = 30   

class CubeCallManager():
    STATE_CREATING = 0
    STATE_QUESTIONING = 1
    STATE_ANSWERING = 2

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("CallManager created")

    def make_call(self, name, number):
        twiml = """
            <Response>
                <Gather input="speech" timeout="5">
                    <Say>Hi {} - This is Hilton from Cube Renovation. Thanks for visiting our site today. 
                  We’d love to offer you a first time customer discount in exchange for your honest feedback to a one-question survey. 
                  Since visiting our site, have you purchased a renovation service from another company or pro? 
                  (If No, say “No”, If Yes, say the name of the company you purchased from).</Say>
                </Gather>
            </Response>
        """.format(name)
        self.call = self.client.calls.create(twiml=twiml, to=number, from_=MY_NUMBER)
        self.calls(self.call.sid).update(url=SERVICE_URL+"/callfollowup/{}".format(self.call.sid))

    def call_follow_up(self, answer, sid):
        if answer.lower() == 'no':
            text = """Cube Renovation provides beautiful, architect-designed renovations completed reliably from start to end.
                      We are offering $2,000 off your bath renovation if you stay on the line to speak to a member of our concierge team who can provide you with a free quote."""
        elif answer.lower() == 'yes':
            text = """We’re sorry to lose your business, and we hope you enjoy your new bathroom."""
        else:
            text = """Thanks for your response. Use code RV20 at checkout to get $500 off if you decide to book with Cube in the future."""
        twiml = "<Response><Say>{}</Say></Response>".format(text)
        self.calls(sid).update(twiml=twiml)        

class CubeScheduler():

    def __init__(self):
        print('Scheduler created')
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.start()
        print("Scheduler created")

    def schedule_call(self, name, number):
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=self.SECONDS_TO_WAIT)
        self.scheduler.add_job(lambda: app.config['callmanager'].make_call(name, number), 'date', run_date=now+delta) 
        print("Calling {} @ {}".format(name, number))