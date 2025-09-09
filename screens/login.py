from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from models.db_con import *
from models.model import auth
from components.wgt import Clock,partial
Builder.load_file(os.path.join(os.path.dirname(__file__),f'login.kv'))

class Login_page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.count_attamt=0
        self.count_num=60
        self.user=None
    def verify_fun_thread(self, *args):
        Thread(target=self.verify_fun_clock, daemon=True).start()
    def verify_fun_clock(self, *args):
        username = self.ids.user1.text
        user = select_one(auth, user=username)
        self.user = user
        Clock.schedule_once(lambda dt: self.verify_login(self.user),1)
    def verify_login(self,user):
        self.user=user
        if self.ids.user1.text and self.ids.pass1.text: 
            if self.user:
                pwd=base64.b64decode(self.user.password).decode('utf-8')
                if self.user.user == self.ids.user1.text and pwd == self.ids.pass1.text:
                    if self.manager.get_screen('token_scr').expire_check(self.user):
                        Clock.schedule_once(partial(self.app.notify,f'Scessfull login'),1)
                        self.ids.user1.text=''
                        self.ids.pass1.text=''
                        self.manager.current='home_scr'
                        self.manager.transition.direction="left"
                    else:
                        self.manager.current='token_scr'
                        self.manager.transition.direction="down"
                else:
                    Clock.schedule_once(partial(self.app.notify,f'Login Faild'),1)
            else:
                Clock.schedule_once(partial(self.app.notify,f'User Name Not valid'),1)
        else:
            Clock.schedule_once(partial(self.app.notify,f'Emty Filld'),1)
        self.ids.user1.text=''
        self.ids.pass1.text=''
        if self.count_attamt == 4:
            self.ids.user1.disabled=True
            self.ids.pass1.disabled=True
            self.ids.Submit_login.disabled=True
            self.count_attamt=0
            self.th1=Clock.schedule_interval(lambda dt:self.update_time(), 1)
        else:
            self.count_attamt+=1
        self.ids.spin.active=False
        Clock.schedule_once(self.manager.get_screen('token_scr').auto_check,1)
        
    def update_time(self,*args):
        self.count_num=self.count_num-1
        self.ids.time_at.text=str(self.count_num)
        if self.count_num == 0:
            self.ids.time_at.text=''
            self.ids.user1.disabled=False
            self.ids.pass1.disabled=False
            self.ids.Submit_login.disabled=False
            Clock.schedule_once(partial(self.app.notify,f'Login agin'),1)
            self.count_num=60
            self.th1.cancel()