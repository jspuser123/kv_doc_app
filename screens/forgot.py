from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from models.db_con import *
from models.model import auth
from components.wgt import Clock
from kivymd.uix.snackbar import Snackbar
Builder.load_file(os.path.join(os.path.dirname(__file__),f'forgot.kv'))

class Forgot_page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.email_data=None
    def on_enter(self, *args):
        self.page_count=0
        self.ids.sending_email.text=''
    def verify_email(self):
        self.ids.spin.active=True
        em=self.ids.sending_email.text
        if em:
            self.email_data=select_one(auth, email=em)
            if self.page_count == 4:
                self.manager.current='login_scr'
                self.manager.transition.direction="right"
            else:
                if self.email_data:
                    if self.email_data.email==em:
                        Thread(target=self.send_otp_fun, args=(self.email_data.email,), daemon=True).start()
                        self.ids.otp_text.opacity=1
                        self.ids.otp_submit.opacity=1
                    else:
                        Snackbar(text="this Not same email").open()
                else:
                    Snackbar(text="Pls enter vaild email").open()
            self.ids.sending_email.text=''
            self.page_count+=1
        else:
            Snackbar(text="Pls enter email").open()
        self.ids.spin.active=False
    def send_otp_fun(self,email):
        if email:
            EMAIL_OTP=self.app.otp_gen()
            msg = EMAIL_OTP + " this is your OTP No Reply Server"
            self.app.send_email(email,msg)
            self.otp_email=EMAIL_OTP
            self.ids.spin.active=False

    def otp_verfiy(self):
        otp=self.ids.otp_text.text
        if self.otp_email==otp:
            em=self.email_data.password
            pwd=base64.b64decode(self.email_data.password).decode('utf-8')
            msg_data=pwd+'this your password'
            self.app.send_email(self.email_data.email,msg_data)
            self.manager.current='login_scr'
            self.manager.transition.direction="right"
            Snackbar(text="verified your email send pwd").open()
        else:
            Snackbar(text="pls Enter correct otp").open()
        self.ids.otp_text.text=''
        self.ids.otp_text.opacity=0
        self.ids.otp_submit.opacity=0