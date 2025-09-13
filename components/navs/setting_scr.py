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
        Clock.schedule_once(self.view_path,1)
    def view_path(self,*args):
        self.path_server=select_one(path_server,id=1) #'//server/SHARING/IT/test'
        self.ids.path_id.text=self.path_server.path
    def save_path(self,*args):
        if self.path_server:
            update_row(path_server,{'id':self.path_server.id},self.ids.path_id.text)
        else:
            insert_row(path_server,path=self.ids.path_id.text)
        self.app.notify(f'Saved path: {self.ids.path_id.text}')
    def delete_path(self,*args):
        delete_row(path_server,id=self.path_server.id)
        self.ids.path_id.text=''
        self.app.notify(f'Deleted path: {self.ids.path_id.text}')
