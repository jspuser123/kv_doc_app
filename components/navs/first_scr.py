from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os,MDDropdownMenu
# from components.tabs.add.tab_1 import Tab_company
from models.model import document_name,document,document_child
from models.db_con import *
Builder.load_file(os.path.join(os.path.dirname(__file__),f'first_scr.kv'))
class Nav_first_scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.nav_manager = ObjectProperty()
        self.from_date=None
        self.to_date=None
    def on_enter(self, *args):
        Clock.schedule_once(self.load, .05)
        Clock.schedule_once(self.document_list, 0.8)
        Clock.schedule_once(self.io_menu_fun, 1)
        Clock.schedule_once(self.stye_menu_fun, 1.1)
        Clock.schedule_once(self.color_menu_fun, 1.2)
        Clock.schedule_once(self.pi_menu_fun, 1.3)
    def on_leave(self, *args):
        if self.app.admob:
            self.app.admob.hide_banner() # hide banner
    def on_kv_post(self, base_widget):
        self.document_data=[]
    def load(self,*args):
        if self.app.admob:
            from utility.ad.my_ids import user_ids
            self.app.admob.load_banner(user_ids.BANNER, top=True)
        self.document_data=select_all(document)
    def document_list(self,*args):
        self.data=[{
            'name':x.name,
            'desc':x.description,
            'io':x.io,  
            'style':x.style,
            'color':x.color,
            'pi':x.pi,
            'date':x.date.strftime('%Y-%m-%d'),
            'value':'',
            'id_data':x.id,
            'delete_card':self.document_delete,
            'view_card':self.document_view,
            'update_card':self.document_update,
            'view_opacity':1,
            'del_opacity':1,
            'update_opacity':1,

            } for x in self.document_data]
        self.ids.list_card.data=self.data
    def document_view(self,*args):
        x=args[0]
        self.nav_manager.current = "view_scr"
        self.nav_manager.get_screen('view_scr').document_view(x)
    def document_delete(self,*args):
        x=args[0]
        with get_session() as session:
            doc = session.query(document).get(x.id_data)
            for child in doc.document_child:
                if os.path.exists(child.file):
                    os.remove(child.file)
            
            session.delete(doc)
            session.commit()
        self.ids.list_card.data.remove({
            'id_data':x.id_data,
            'name':x.name,
            'desc':x.desc,
            'io':x.io,
            'style':x.style,
            'color':x.color,
            'pi':x.pi,
            'value':'',
            'date':x.date,
            'delete_card':self.document_delete,
            'view_card':self.document_view,
            'update_card':self.document_update,
            'view_opacity':1,
            'del_opacity':1,
            'update_opacity':1,
            })
        # self.ids.list_card.data.pop()
        
    def document_update(self,*args):
        x=args[0]
        self.nav_manager.current = "add_scr"
        self.nav_manager.get_screen('add_scr').document_update_data(x)
    def from_date_fun(self,*args):
        self.ids.from_date_id.text=str(args[1])
        self.from_date = args[1]
    def to_date_fun(self,*args):
        self.ids.to_date_id.text=str(args[1])
        self.to_date = args[1]
    def io_menu_fun(self,*args):
        menu_items = [
            {
                "text": f"{i.io}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i.io: self.io_callback(x),
            } for i in self.document_data
        ]
        self.io_menu = MDDropdownMenu(
            caller=self.ids.io_id,
            items=menu_items,
            position="bottom",
            width_mult=3,
            background_color=self.app.theme_cls.primary_light,
            hor_growth="left",
        )
    def text_change(self,*args):####this change fun filter
        value=args[0]
        if not value:
            return
        # filtered_items = [
        #     {
        #         "text": f"Io: {i.io}",
        #         "viewclass": "OneLineListItem",
        #         "on_release": lambda x=i.io: self.io_callback(x),
        #     } for i in  self.document_data if value.lower() in i.io.lower()
        # ]
        # self.io_menu.items = filtered_items
        # self.io_menu.open()

    def io_callback(self, text_item):
        self.ids.io_id.text_in.text=text_item
        self.io_menu.dismiss()
    def stye_menu_fun(self,*args):
        menu_items = [
            {
                "text": f"{i.style}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i.style: self.stye_callback(x),
            } for i in self.document_data
        ]
        self.style_menu = MDDropdownMenu(
            caller=self.ids.style_id,
            items=menu_items,
            position="bottom",
            width_mult=3,
            background_color=self.app.theme_cls.primary_light,
            hor_growth="right",
        )
    def stye_callback(self, text_item):
        self.ids.style_id.text_in.text=text_item
        self.style_menu.dismiss()
    def color_menu_fun(self,*args):
        menu_items = [
            {
                "text": f"{i.color}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i.color: self.color_callback(x),
            } for i in self.document_data
        ]
        self.color_menu = MDDropdownMenu(
            caller=self.ids.color_id,
            items=menu_items,
            position="bottom",
            width_mult=3,
            background_color=self.app.theme_cls.primary_light,
            hor_growth="right",
        )
    def color_callback(self, text_item):
        self.ids.color_id.text_in.text=text_item
        self.color_menu.dismiss()
    def pi_menu_fun(self,*args):
        menu_items = [
            {
                "text": f"{i.pi}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i.pi: self.pi_callback(x),
            } for i in self.document_data
        ]
        self.pi_menu = MDDropdownMenu(
            caller=self.ids.pi_id,
            items=menu_items,
            position="bottom",
            width_mult=3,
            background_color=self.app.theme_cls.primary_light,
            hor_growth="right",
        )
    def pi_callback(self, text_item):
        self.ids.pi_id.text_in.text=text_item
        self.pi_menu.dismiss()
   
    def search_fun(self, *args):
        search = self.ids.search_id.text_in.text
        io = self.ids.io_id.text_in.text
        style = self.ids.style_id.text_in.text
        color = self.ids.color_id.text_in.text
        pi = self.ids.pi_id.text_in.text
        filters = {
            'date': (self.from_date, self.to_date),
            'io': io,
            'style': style,
            'color': color,
            'pi': pi,
            'search': search
        }
        search_data = [i for i in self.data if self.apply_filters(i, filters)]
        self.ids.list_card.data = search_data
    def apply_filters(self, item, filters):
        date_filter = filters['date']
        if date_filter[0] and date_filter[1]:
            if not (date_filter[0] <= datetime.strptime(item['date'], '%Y-%m-%d').date() <= date_filter[1]):
                return False
        io_filter = filters['io']
        if io_filter and io_filter not in item['io']:
            return False
        style_filter = filters['style']
        if style_filter and style_filter not in item['style']:
            return False
        color_filter = filters['color']
        if color_filter and color_filter not in item['color']:
            return False
        pi_filter = filters['pi']
        if pi_filter and pi_filter not in item['pi']:
            return False
        search_filter = filters['search']
        if search_filter and (search_filter not in item['name'] and search_filter not in item['desc']):
            return False
        return True
    def clear_fun(self,*args):
        self.ids.search_id.text_in.text=''
        self.ids.io_id.text_in.text=''
        self.ids.style_id.text_in.text=''
        self.ids.color_id.text_in.text=''
        self.ids.pi_id.text_in.text=''
        self.ids.from_date_id.text='From date'
        self.ids.to_date_id.text='To date'
        self.from_date=None
        self.to_date=None
        Clock.schedule_once(self.document_list, 0.8)
     # def search_fun(self,*args):
    #     search=self.ids.search_id.text_in.text
    #     io=self.ids.io_id.text_in.text
    #     style=self.ids.style_id.text_in.text
    #     color=self.ids.color_id.text_in.text
    #     pi=self.ids.pi_id.text_in.text
    #     if self.from_date and self.to_date and io and style and color and pi and search:    
    #         search_data=[i for i in self.data if  (self.from_date <= datetime.strptime(i['date'], '%Y-%m-%d').date() <= self.to_date) and (io in i['io']) and (style in i['style'])  and (color in i['color']) and (pi in i['pi']) and (search in str(i['value']) or search in i['name'] or search in i['desc'])]
    #         self.ids.list_card.data=search_data
    #         print('all')
    #     elif self.from_date and self.to_date and io and style and color and pi:    
    #         search_data=[i for i in self.data if  (self.from_date <= datetime.strptime(i['date'], '%Y-%m-%d').date() <= self.to_date) and (io in i['io']) and (style in i['style'])  and (color in i['color']) and (pi in i['pi'])]
    #         self.ids.list_card.data=search_data
    #         print('date+io+style+color+pi')
    #     elif self.from_date and self.to_date and io and style and color:    
    #         search_data=[i for i in self.data if  (self.from_date <= datetime.strptime(i['date'], '%Y-%m-%d').date() <= self.to_date) and (io in i['io']) and (style in i['style'])  and (color in i['color']) ]
    #         self.ids.list_card.data=search_data
    #         print('date+io+style+color')
    #     elif self.from_date and self.to_date and io and style:    
    #         search_data=[i for i in self.data if  (self.from_date <= datetime.strptime(i['date'], '%Y-%m-%d').date() <= self.to_date) and (io in i['io']) and (style in i['style'])]
    #         self.ids.list_card.data=search_data
    #         print('date+io+style')
    #     elif self.from_date and self.to_date and io:    
    #         search_data=[i for i in self.data if  (self.from_date <= datetime.strptime(i['date'], '%Y-%m-%d').date() <= self.to_date) and (io in i['io'])]
    #         self.ids.list_card.data=search_data
    #         print('date+io')
    #     elif self.from_date and self.to_date:
    #         search_data=[i for i in self.data if  (self.from_date <= datetime.strptime(i['date'], '%Y-%m-%d').date() <= self.to_date)]
    #         self.ids.list_card.data=search_data
    #         print('date')
    #     elif io and style and color and pi:    
    #         search_data=[i for i in self.data if  (io in i['io']) and (style in i['style'])  and (color in i['color']) and (pi in i['pi'])]
    #         self.ids.list_card.data=search_data
    #         print('io+style+color+pi')
    #     elif style and color and pi:    
    #         search_data=[i for i in self.data if  (style in i['style'])  and (color in i['color']) and (pi in i['pi'])]
    #         self.ids.list_card.data=search_data
    #         print('style+color+pi')
    #     elif color and pi:    
    #         search_data=[i for i in self.data if (color in i['color']) and (pi in i['pi'])]
    #         self.ids.list_card.data=search_data
    #         print('color+pi')
    #     elif io:    
    #         search_data=[i for i in self.data if (io in i['io'])]
    #         self.ids.list_card.data=search_data
    #         print('io')
    #     elif style:    
    #         search_data=[i for i in self.data if (style in i['style'])]
    #         self.ids.list_card.data=search_data
    #         print('style')
    #     elif color:
    #         search_data=[i for i in self.data if (color in i['color'])]
    #         self.ids.list_card.data=search_data
    #         print('color')
    #     elif pi:    
    #         search_data=[i for i in self.data if (pi in i['pi'])]
    #         self.ids.list_card.data=search_data
    #         print('pi')
    #     elif search:
    #         search_data=[i for i in  self.data if search in str(i['value']) or search in i['name'] or search in i['desc']]
    #         self.ids.list_card.data=search_data
    #         print('search')
    #     self.salary_print_data=search_data
        #if x.name.lower().find(self.ids.search_id.text_in.text.lower())!=-1 or x.description.lower().find(self.ids.search_id.text_in.text.lower())!=-1 or x.io.lower().find(self.ids.io_id.text_in.text.lower())!=-1 or x.style.lower().find(self.ids.style_id.text_in.text.lower())!=-1 or x.color.lower().find(self.ids.color_id.text_in.text.lower())!=-1 or x.pi.lower().find(self.ids.pi_id.text_in.text.lower())!=-1