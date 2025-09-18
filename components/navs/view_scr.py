from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os,Items_Card,Animation,TwoLineAvatarIconListItem,IconLeftWidget,IconRightWidget,webbrowser
# from components.tabs.add.tab_1 import Tab_company
from models.model import document_name,document,document_child
from models.db_con import *
Builder.load_file(os.path.join(os.path.dirname(__file__),f'view_scr.kv'))
class Nav_view_scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.nav_manager = ObjectProperty()
    def document_view(self,*args):
        self.ids.view_cards.clear_widgets()
        x=args[0]
        card=Items_Card()
        card.name=x.name
        card.desc=x.desc
        card.io=x.io
        card.style=x.style
        card.color=x.color
        card.pi=x.pi
        card.value=x.value
        card.date=x.date
        card.id_data=x.id
        card.opacity=0
        card.view_opacity=0
        card.del_opacity=0
        self.ids.view_cards.add_widget(card)
        Animation(opacity=1,d=.5,t='out_quad').start(card)
        x=select_all(document_child,document_id=x.id_data)
        if x:
            for i in x:
                self.ids.view_cards.add_widget(TwoLineAvatarIconListItem(
                                                                        IconLeftWidget(
                                                                            icon="database"
                                                                        ),
                                                                        IconRightWidget(
                                                                            icon="arrow-right",
                                                                            on_release=partial(self.document_load,i.document_id,i.name,i.file),
                                                                        ),
                                                                        
                                                                        id=str(i.document_id),
                                                                        text=i.name,
                                                                        secondary_text=i.file,
                                                                        ))
    def document_load(self,*args):
        print(args)
        id=args[0]
        name=args[1]
        link=args[2]
        # webbrowser.open(link)
        # file_path = 
        os.startfile(r'file:///'+link)



