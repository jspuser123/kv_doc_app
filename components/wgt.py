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
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.tab import MDTabsBase
from kivy.properties import *
from kivymd.uix.list import OneLineAvatarIconListItem,IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.animation import Animation
from kivymd.uix.behaviors import HoverBehavior,ScaleBehavior
import random
import os
import sys
from hashlib import sha256
import math
from threading import Thread
from datetime import datetime

Builder.load_file(os.path.join(os.path.dirname(__file__),f'wgt.kv'))
class Lbl1(MDLabel):
    pass
class Spiner(MDSpinner):
    pass
class Textboxcustom(MDBoxLayout):
    pass
class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
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