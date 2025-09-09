from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from models.db_con import *
from models.model import auth
from components.wgt import Clock,partial
Builder.load_file(os.path.join(os.path.dirname(__file__),f'verfy.kv'))

class Verify_page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.verify=None
        self.app=MDApp.get_running_app()
    def on_enter(self, *args):
        self.time_val=200
        Clock.schedule_once(self.time_fun,1)
    def verify_fun(self):
        self.ids.spin.active=True
        email=self.manager.get_screen('reg_scr').otp_email
        e1,e2,e3,e4=self.ids.e1.text,self.ids.e2.text,self.ids.e3.text,self.ids.e4.text,
        if e1 and e2 and e3 and e4:
            em_ver=e1+e2+e3+e4
            if em_ver == email:
                self.verify=True
                user=self.manager.get_screen('reg_scr').ids.username.text
                pass1=self.manager.get_screen('reg_scr').ids.pass1.text
                ph=self.manager.get_screen('reg_scr').ids.phone.text
                email_data=self.manager.get_screen('reg_scr').ids.email.text
                company_data=self.manager.get_screen('reg_scr').ids.company.text
                in_date=datetime.now()
                ex_date=datetime.now()+timedelta(days=365) ########## expire altre #########
                try: 
                    data_pwd = base64.b64encode(pass1.encode('utf-8'))
                    Thread(target=self.regsistor_fun, args=(user,data_pwd,email_data,ph,in_date,ex_date,company_data), daemon=True).start()
                except:
                    print('regsistor error')
                self.ids.e1.text='';self.ids.e2.text='';self.ids.e3.text='';self.ids.e4.tex=''
                Clock.schedule_once(partial(self.app.notify,f"Successful Register ..!"),1)
                self.manager.current='login_scr'
                self.manager.transition.direction="right"
            else:
                Clock.schedule_once(partial(self.app.notify,f"OTP Faild"),1)
                self.ids.spin.active=False
        else:
            Clock.schedule_once(partial(self.app.notify,f"OTP EMTYFILD"),1)
            self.ids.spin.active=False
    def regsistor_fun(self,user,data_pwd,email_data,ph,in_date,ex_date,company_data):
        token=self.manager.get_screen('token_scr').token_gen(company_data)
        data=insert_row(auth, user=user, password=data_pwd, email=email_data, ph=ph, init_date=in_date, expire_date=ex_date, company=company_data,token=token,version=0)
        self.ids.spin.active=False
    def resend_otp(self):
        eml=self.manager.get_screen('reg_scr').ids.email.text
        self.manager.get_screen('reg_scr').email_otp_fun(eml)
        self.th.cancel()
        self.on_enter()
    def time_fun(self,dt):
        self.th=Clock.schedule_interval(lambda dt:self.update_time(), 1)
    def update_time(self,*args):
        self.time_val=self.time_val-1
        self.ids.time_id.text=str(self.time_val)
        if self.time_val == 0:
            Clock.schedule_once(partial(self.app.notify,f"Time out"),1)
            self.manager.current='reg_scr'
            self.manager.transition.direction="right"
    def on_leave(self, *args):
        for key, val in  self.manager.get_screen('reg_scr').ids.items():
            val.text=''
        self.ids.time_id.text=''
        self.th.cancel()