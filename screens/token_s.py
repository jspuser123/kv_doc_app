import re
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from models.db_con import *
from models.model import auth
from components.wgt import Clock,partial
from hashlib import sha256
Builder.load_file(os.path.join(os.path.dirname(__file__),f'token_s.kv'))

class Token_page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.user=None
        self.token=None
    def on_enter(self, *args):
        pass

    def auto_check(self,*args):
        self.user=select_all(auth)
        if self.user:
            for data in self.user:
                if self.expire_check(data) ==False:
                    Clock.schedule_once(partial(self.app.notify,f'Expire token contect admin!'),1)
        Clock.schedule_once(self.auto_check,86400)
    def expire_check(self,user):
        try:
            init_date = datetime.strptime(str(user.init_date), "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            init_date = datetime.strptime(str(user.init_date), "%Y-%m-%d %H:%M:%S")
        try:
            expire_date = datetime.strptime(str(user.expire_date), "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            expire_date = datetime.strptime(str(user.expire_date), "%Y-%m-%d %H:%M:%S")
        dexpiration = (expire_date - datetime.now()).days
        token=sha256(f'{user.company}:{datetime.now().year}asp@321'.encode('utf-8')).hexdigest()
        # token=sha256(f'{user.company}:{datetime.now().month}asp@321'.encode('utf-8')).hexdigest()
        if dexpiration>=1 and token == user.token:
            return True
        else: 
            return False
    def token_gen(self,*args):
        try: 
            t=datetime.now()
            ins=f'{args[0]}:{t.year}asp@321'
            self.token=sha256(ins.encode('utf-8')).hexdigest()
            return self.token
        except Exception as e:
            self.app.notify(f'token error{e}')
            return 'No Token'
    def verify_token(self):
        self.ids.spin.active=True
        ex_date=datetime.now()+timedelta(days=365) 
        if self.user:
            if self.token_gen(self.user[0].company) == self.ids.token_text.text:
                for u in self.user:
                    u.expire_date = ex_date
                    Thread(target=self.token_fun_th, args=(u.id,ex_date,self.ids.token_text.text,),daemon=True).start()
            Clock.schedule_once(partial(self.app.notify,f'token accepted!'),1)
            self.manager.current='login_scr'
        else:  
            Clock.schedule_once(partial(self.app.notify,f'Token not accepted!'),1)
        self.ids.spin.active=False
    def token_fun_th(self,id,ex_date,token):
        update_row(auth,{'id':id},{'expire_date':ex_date,'token':token})
