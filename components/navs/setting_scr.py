from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os
from models.model import path_server
from models.db_con import *
Builder.load_file(os.path.join(os.path.dirname(__file__),f'setting_scr.kv'))
class Nav_setting_scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.nav_manager = ObjectProperty()
        self.path_server=None
    def on_enter(self, *args):
        Clock.schedule_once(self.enable_disable_dialog,0.5)
    def on_leave(self, *args):
        if self.app.nav_dialog:
            self.app.nav_dialog.dismiss()
    def enable_disable_dialog(self,*args):
        self.app.show_setting_dialog(self.verify_and_close_dialog,'Devlop Admin Only!',self.nav_app_return_menu)
    def verify_and_close_dialog(self, *args):
        text_value =  self.app.nav_dialog.content_cls.ids.nav_pass.text
        if text_value == "9786asp9786":
            self.app.nav_dialog.dismiss()
            Clock.schedule_once(partial(self.app.notify,f'Verified Sucess'),1)
            Clock.schedule_once(self.view_path,0.3)
        else:
           Clock.schedule_once(partial(self.app.notify,f'Verification failed'),1)
    def nav_app_return_menu(self,*args):
        self.nav_manager.current = 'first_scr'
    def view_path(self,*args):
        self.path_server=select_one(path_server,id=1) #'//server/SHARING/IT/test'
        self.ids.path_id.text=self.path_server.path if self.path_server else ''
    def save_path(self,*args):
        if self.path_server:
            update_row(path_server,{'id':1},{'path':self.ids.path_id.text})
        else:
            insert_row(path_server,path=self.ids.path_id.text)
        self.app.notify(f'Saved path: {self.ids.path_id.text}')
    def delete_path(self,*args):
        delete_row(path_server,id=1)
        self.ids.path_id.text=''
        self.app.notify(f'Deleted path: {self.ids.path_id.text}')
