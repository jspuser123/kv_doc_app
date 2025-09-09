from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os
from components.tabs.add.tab_1 import Tab_company

Builder.load_file(os.path.join(os.path.dirname(__file__),f'first_scr.kv'))
class Nav_first_scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.nav_manager = ObjectProperty()
        self.nav_drawer = ObjectProperty()
    def on_enter(self, *args):
        Clock.schedule_once(self.load, 1)
    def on_leave(self, *args):
        if self.app.admob:
            self.app.admob.hide_banner() # hide banner
    def load(self,*args):
        if self.app.admob:
            from utility.ad.my_ids import user_ids
            self.app.admob.load_banner(user_ids.BANNER, top=True)