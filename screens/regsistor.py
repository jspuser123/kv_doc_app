from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from models.db_con import *
from models.model import auth
from components.wgt import Clock,partial
Builder.load_file(os.path.join(os.path.dirname(__file__),f'regsistor.kv'))

class Regsistor_page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.otp_sms=None
        self.otp_email=None
        self.otp_server=None
    def reg_fun(self):
        self.ids.spin.active=True
        user_count = count_rows(auth, auth.id)
        usr,p1,p2,ph,eml,comp=self.ids.username.text,self.ids.pass1.text,self.ids.pass2.text,self.ids.phone.text,self.ids.email.text,self.ids.company.text
        if user_count<=5: 
            if usr and p1 and p2 and ph and eml and comp:
                if p1 == p2:
                    self.email_otp_fun(eml)
                    self.manager.current='verify_scr'
                    self.manager.transition.direction="left"
                else:
                    Clock.schedule_once(partial(self.app.notify,f"Password don't Match"),1)
            else:
                Clock.schedule_once(partial(self.app.notify,f"Emty Filled"),1)
        else:
            Clock.schedule_once(partial(self.app.notify,f"Only three users allowed"),1)
        self.ids.spin.active=False
    def email_otp_fun(self,eml):
        self.otp_email=None
        self.otp_server=None
        if eml:
            EMAIL_OTP=self.app.otp_gen()
            msg = EMAIL_OTP + "\n this is login your app \n"+str(datetime.now())
            Thread(target=self.app.send_email, args=(eml,msg), daemon=True).start()
            self.otp_email=EMAIL_OTP


