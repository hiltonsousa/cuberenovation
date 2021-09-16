from apscheduler.schedulers.background import BackgroundScheduler
import datetime

TWILIO_ACCOUNT_SID = 'AC37b0224ede54804a1b1a597e2fa208d0'
TWILIO_AUTH_TOKEN = 'e28f18fec5ebee7833d782dbfefe4393'
MY_NUMBER = '+15707052076'

class CubeRenovationScheculer():
    SECONDS_TO_WAIT = 30   

    def __init__(self):
        print('Scheduler created')
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.start()

    def schedule_call(self, name, number):
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=self.SECONDS_TO_WAIT)
        self.scheduler.add_job(lambda: self.call_twilio(name, number), 'date', run_date=now+delta) 

    def call_twilio(self, name, number):
        print("Calling {} @ {}".format(name, number))