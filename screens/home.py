from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,os,Builder
from components.navs.first_scr import Nav_first_scr

Builder.load_file(os.path.join(os.path.dirname(__file__),f'home.kv'))
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()