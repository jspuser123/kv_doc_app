from components.wgt import MDApp,Builder,MDBoxLayout,MDCard,HoverBehavior,Image,Clock,partial,random,Thread,os
from kivy.properties import *


Builder.load_file(os.path.join(os.path.dirname(__file__),f'custom_tbl.kv'))
class Cus_Tbl_tob_wgt(MDBoxLayout):
    search_text=StringProperty()
    press_search=ObjectProperty()
    def item_search_fun(self,*args):
        self.search_text=self.ids.item_search.text
        self.press_search(self.search_text)
class Items_Card(MDCard,HoverBehavior):
    no = StringProperty()
    source = StringProperty('')
    dapartment=StringProperty()
    name = StringProperty()
    person_id = StringProperty()
    designation =StringProperty()
    genter =StringProperty()
    contact = StringProperty()
    doj = StringProperty()
    city = StringProperty()
    md_bg_color = ColorProperty([1, 1, 1, 1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_data=ObjectProperty()
        self.chk_id=ObjectProperty()
        self.update_card = ObjectProperty(None)
        self.on_card_press_item=ObjectProperty()
        self.on_press_delete=ObjectProperty()
    def on_enter(self, *args):
        self.line_color='grey'
        self.md_bg_color="#FCF7FC"
    def on_leave(self, *args):
        self.md_bg_color=self.random_light_color()
        self.line_color='#E6E6E6'
    def on_press_card(self, *args):
        # Call a callback on the parent or app
        app = MDApp.get_running_app()
        if hasattr(self.parent, "on_card_pressed"):
            app.root.on_card_pressed(self)
    def update_card_item(self,*args):
        if self.update_card:
            self.update_card(self)
    def random_light_color(self):
        r = random.uniform(0.7, 1.0)
        g = random.uniform(0.7, 1.0)
        b = random.uniform(0.7, 1.0)
        return [r, g, b, 1]
    def on_press_card(self, *args):
        # Call a callback on the parent or app
        app = MDApp.get_running_app()
        if hasattr(app.root, "on_card_pressed"):
            app.root.on_card_pressed(self)
        print('yes press')
    def card_press_fun(self, *args):
        if self.on_card_press_item:
            self.on_card_press_item(self)
    def delete_row_thread(self,*args):
        if self.on_press_delete:
            self.on_press_delete(self.id_data,self.source)
class  Cus_tbl(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app=MDApp.get_running_app()
        self.tab_user_add=ObjectProperty()
    def on_kv_post(self, base_widget):
        Thread(target=self.all_data_added,daemon=True).start()
    def all_data_added(self,*args):
        Clock.schedule_once(self.user_datas,1)
    def user_datas(self,*args):
        self.data=None# select_all(person)
        self.page_size = 5
        self.current_page = 0 
        self.all_items=[
            {'no':str(x.id),
             'id_data':str(x.person_id),
             'source':x.person_image if x else 'assets/images/data_img/profile/face.jpg',
             'dapartment':x.person_deparment,
             'name':x.person_name,
             'person_id':str(x.person_id),
             'designation':x.person_designation,
             'genter':x.person_genter,
             'contact':str(x.person_contact),
             'doj':str(x.person_d_o_p),
             'city':x.person_city,
             'md_bg_color':(self.random_light_color()),
             'on_card_press_item':self.update_pass_data,
             'on_press_delete':self.delete_pass_id
            } for x in self.data
            ]
        self.update_page()

    def update_page(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        self.ids.items_tbl_card.data = self.all_items[start:end]
        total_pages = (len(self.all_items) + self.page_size - 1) // self.page_size
        self.ids.page_status.text = f"{start + 1} - {min(end, len(self.all_items))} OF {len(self.all_items)} (Page {self.current_page + 1} / {total_pages})"

    def page_prves(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def page_next(self):
        total_pages = (len(self.all_items) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_page()
    def update_pass_data(self,*args):
        person_id=args[0].id_data
        self.tab_user_add.edit_person_data(person_id)
       # self.app.root.get_screen('home_scr').ids.nav_sm.get_screen('nav_add_user').edit_person_data(person_data)
    def delete_pass_id(self,*args):
        person_id=args[0]
        img_source=args[1]
        self.app.dia_close_fun()
        self.tab_user_add.fun_send('delete',person_id,img_source)
        Clock.schedule_once(self.user_datas,1)
        #Clock.schedule_once(partial(self.app.noty_fy_send,f'delete row sucess fully'),1)
    def random_light_color(self):
        r = random.uniform(0.7, 1.0)
        g = random.uniform(0.7, 1.0)
        b = random.uniform(0.7, 1.0)
        return [r, g, b, 1]
    def text_search_fun(self,*args):
        data = [y for y in self.data if args[0].lower() in y.person_name.lower() or args[0] in str(y.person_id)]
        self.page_size = 5
        self.current_page = 0 
        self.all_items=[
            {'no':str(x.id),
             'id_data':str(x.person_id),
             'source':x.person_image if x else 'assets/images/data_img/profile/face.jpg',
             'dapartment':x.person_deparment,
             'name':x.person_name,
             'person_id':str(x.person_id),
             'designation':x.person_designation,
             'genter':x.person_genter,
             'contact':str(x.person_contact),
             'doj':str(x.person_d_o_p),
             'city':x.person_city,
             'md_bg_color':(self.random_light_color()),
             'on_card_press_item':self.update_pass_data,
             'on_press_delete':self.delete_pass_id
            } for x in data
            ]
        self.update_page()