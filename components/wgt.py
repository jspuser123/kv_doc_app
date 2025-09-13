from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.utils import platform
from kivy.clock import Clock
from functools import partial
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.recycleview import RecycleView
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import *
from kivymd.uix.list import OneLineAvatarIconListItem,IRightBodyTouch,TwoLineAvatarIconListItem,IconLeftWidget,IconRightWidget
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.animation import Animation
from kivymd.uix.behaviors import HoverBehavior,ScaleBehavior
from kivymd.uix.menu import MDDropdownMenu
from plyer import filechooser
import random
import os
import sys
from hashlib import sha256
import math
from threading import Thread
from datetime import datetime
import shutil


Builder.load_file(os.path.join(os.path.dirname(__file__),f'wgt.kv'))
class Lbl1(MDLabel):
    pass
class Spiner(MDSpinner):
    pass
class Textboxcustom(MDBoxLayout):
    pass
class Line_text(MDBoxLayout):
    fouces=BooleanProperty(False)
    in_text=StringProperty()
    text_call=ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_focus(self,*args):
        self.fouces=True
        self.ids.text_in.focus=True
    def call_text(self,*args):
        self.text_call(self.in_text)

class DialogContent(MDBoxLayout):
    pass
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass
class List_item(OneLineAvatarIconListItem):
    pass
class About_card(MDCard):
    source = StringProperty('')
    icn_color = ColorProperty([1, 1, 1, 1])
    text = StringProperty()
    text_color = ColorProperty([1, 1, 1, 1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
class Nav_list(OneLineAvatarIconListItem,HoverBehavior):
    def on_enter(self, *args):
        self.bg_color="white"
        self.text_color='blue'
        self.ids.right_i.text_color='blue'
    def on_leave(self, *args):
        self.bg_color='#181824'
        self.text_color='white'
        self.ids.right_i.text_color='#181824'
class SelectCardRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Items_Card(MDCard,HoverBehavior):
    no = StringProperty()
    name = StringProperty()
    desc = StringProperty()
    io = StringProperty()
    style=StringProperty()
    color =StringProperty()
    style =StringProperty()
    pi = StringProperty()
    date = StringProperty()
    value = StringProperty()
    md_bg_color = ColorProperty([1, 1, 1, 1])
    delete_card = ObjectProperty()
    update_card = ObjectProperty()
    view_card = ObjectProperty()
    del_opacity = NumericProperty(0)
    view_opacity = NumericProperty(0)
    update_opacity = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_data=ObjectProperty()
        self.chk_id=ObjectProperty()
    def on_enter(self, *args):
        self.md_bg_color="#FCF7FC"
    def on_leave(self, *args):
        self.md_bg_color=self.random_light_color()
    def on_press_card(self, *args):
        # Call a callback on the parent or app
        app = MDApp.get_running_app()
        if hasattr(self.parent, "on_card_pressed"):
            app.root.on_card_pressed(self)
    def view_card_item(self,*args):
        if self.view_card:
            self.view_card(self)
    def update_card_item(self,*args):
        if self.update_card:
            self.update_card(self)
    def delete_card_item(self,*args):
        if self.delete_card:
            self.delete_card(self)
        
    def random_light_color(self):
        r = random.uniform(0.7, 1.0)
        g = random.uniform(0.7, 1.0)
        b = random.uniform(0.7, 1.0)
        return [r, g, b, 1]
        
    # def on_press_card(self, *args):
    #     if self.on_card_press_callback:
    #         self.on_card_press_callback(self)
class ClientsTable(MDBoxLayout):
    def __init__(self, list_col,pageing,**kwargs):
        super().__init__(**kwargs) 
        self.data_tables = None
        self.list_col=list_col
        self.pageing=pageing
        self.create_table(self.list_col, [],pageing)

    def create_table(self, columns, rows,pageing):
        if self.data_tables:
            self.remove_widget(self.data_tables)
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint_x=(.96),
            use_pagination=pageing,
            check=True,
            elevation=0,
            column_data=columns,
            row_data=rows,
        )
        self.add_widget(self.data_tables)