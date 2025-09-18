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
        self.page_size = 100
        self.current_page = 0
        self.menu_page_size = 50
        self.menu_current_page = 0
    def on_enter(self, *args):
        Clock.schedule_once(self.load, .05)
        Clock.schedule_once(self.document_list, 0.8)
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
        #self.ids.list_card.data=self.data
        Clock.schedule_once(self.update_page,0.2)
    def document_view(self,*args):
        x=args[0]
        self.nav_manager.current = "view_scr"
        self.nav_manager.get_screen('view_scr').document_view(x)
    def document_delete(self,*args):
        if self.app.alert_dialog:
            self.app.on_alret_dismiss()
        x=args[0]
        try:
            with get_session() as session:
                doc = session.query(document).get(x.id_data)
                for child in doc.document_child:
                    if os.path.exists(child.file):
                        os.remove(child.file)
                
                session.delete(doc)
                session.commit()
            self.data.remove({
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
        except Exception as e:
            Clock.schedule_once(partial(self.app.notify,f'Error: {e}'),1)
            return
        # self.ids.list_card.data.pop()
        Clock.schedule_once(self.update_page,0.5)
        Clock.schedule_once(partial(self.app.notify,f'Document {x.name} deleted'),1)
    def document_update(self,*args):
        x=args[0]
        if self.app.alert_dialog:
            self.app.on_alret_dismiss()
        self.nav_manager.current = "add_scr"
        self.nav_manager.get_screen('add_scr').document_update_data(x)

    ######table function pagenation#######
    def update_page(self,*args):
        start = self.current_page * self.page_size
        end = start + self.page_size
        if args[0]=='search':
            self.ids.list_card.data=args[1]
            total_pages = (len(args[1]) + self.page_size - 1) // self.page_size
            self.ids.card_page_status.text = f"Results: {len(args[1])}"
        else:
            self.ids.list_card.data = self.data[start:end]
            total_pages = (len(self.data) + self.page_size - 1) // self.page_size
            self.ids.card_page_status.text = f"{start + 1} - {min(end, len(self.data))} OF {len(self.data)} (Page {self.current_page + 1} / {total_pages})"

    def page_prves(self,*args):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def page_next(self,*args):
        total_pages = (len(self.data) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_page()
    ######table function pagenation#######
    def from_date_fun(self,*args):
        self.ids.from_date_id.text=str(args[1])
        self.from_date = args[1]
    def to_date_fun(self,*args):
        self.ids.to_date_id.text=str(args[1])
        self.to_date = args[1]
    ######menu pagenation#######
    def menu_update_page(self,*args):
        start = self.menu_current_page * self.menu_page_size
        end = start + self.menu_page_size
        if args[0]=='search':
            self.app.show_menu.content_cls.data=args[1]
            self.app.show_menu.content_cls.status= f"Result: {len(args[1])}"
        else:
            self.app.show_menu.content_cls.data= args[1][start:end]
            self.app.show_menu.content_cls.status= f"{start + 1} - {min(end, len(args[1]))} OF {len(args[1])}"
    def menu_page_prve(self,*args):
        if self.menu_current_page > 0:
            self.menu_current_page -= 1
            self.menu_update_page('prev')
    def menu_page_next(self,*args):
        total_pages = (len(self.data) + self.menu_page_size - 1) // self.menu_page_size
        if self.menu_current_page < total_pages - 1:
            self.menu_current_page += 1
            self.menu_update_page('next')
    ######menu pagenation#######

    def load_menu_fun(self,*args):
        if args[0]=='io':
            data=[{'text':x.io,'on_press':partial(self.load_item_text_box,'io',x.io)} for x in self.document_data]
            Clock.schedule_once(partial(self.menu_update_page,'io',data),0.5)
        elif args[0]=='style':
            data=[{'text':x.style,'on_press':partial(self.load_item_text_box,'style',x.style)} for x in self.document_data]
            Clock.schedule_once(partial(self.menu_update_page,'style',data),0.5)
        elif args[0]=='color':
            data=[{'text':x.color,'on_press':partial(self.load_item_text_box,'color',x.color)} for x in self.document_data]
            Clock.schedule_once(partial(self.menu_update_page,'color',data),0.5) 
        elif args[0]=='pi':
            data=[{'text':x.pi,'on_press':partial(self.load_item_text_box,'pi',x.pi)} for x in self.document_data]
            Clock.schedule_once(partial(self.menu_update_page,'pi',data),0.5)
    def load_item_text_box(self,*args):
        if args[0]=='io':
            self.ids.io_id.text_in.text=args[1]
        elif args[0]=='style':
            self.ids.style_id.text_in.text=args[1]
        elif args[0]=='color':
            self.ids.color_id.text_in.text=args[1]
        elif args[0]=='pi':
            self.ids.pi_id.text_in.text=args[1]
        self.app.show_menu_on_dismiss()
    def on_submit_menu(self,*args):
        if self.app.show_menu.title in 'IO List':
            self.ids.io_id.text_in.text=self.app.show_menu.content_cls.ids['search_text'].text
        elif self.app.show_menu.title in 'style List':
            self.ids.style_id.text_in.text=self.app.show_menu.content_cls.ids['search_text'].text
        elif self.app.show_menu.title in 'color List':
            self.ids.color_id.text_in.text=self.app.show_menu.content_cls.ids['search_text'].text
        elif self.app.show_menu.title in 'pi List':
            self.ids.pi_id.text_in.text=self.app.show_menu.content_cls.ids['search_text'].text  
        self.app.show_menu_on_dismiss()
    def search_io_fun(self,*args):
        self.app.show_menu.content_cls.load_spinner=True
        self.txt=args[0]
        data=[{'text':x.io,'on_press':partial(self.load_item_text_box,'io',x.io)} for x in self.document_data if x.io.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)
    def search_style_fun(self,*args):
        self.app.show_menu.content_cls.load_spinner=True
        self.txt=args[0]
        data=[{'text':x.style,'on_press':partial(self.load_item_text_box,'style',x.style)} for x in self.document_data if x.style.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)
    def search_color_fun(self,*args):
        self.app.show_menu.content_cls.load_spinner=True
        self.txt=args[0]
        data=[{'text':x.color,'on_press':partial(self.load_item_text_box,'color',x.color)} for x in self.document_data if x.color.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)
    def search_pi_fun(self,*args):
        self.app.show_menu.content_cls.load_spinner=True
        self.txt=args[0]
        data=[{'text':x.pi,'on_press':partial(self.load_item_text_box,'pi',x.pi)} for x in self.document_data if x.pi.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)

    ############search function############
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
        Clock.schedule_once(partial(self.update_page,'search',search_data),0.2)
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
    ############search function############
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
 