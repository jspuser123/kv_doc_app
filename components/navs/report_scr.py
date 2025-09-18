from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os,ClientsTable,dp,MDDropdownMenu
from models.model import document_name,document,document_child,path_server
from models.db_con import *
# from components.tabs.add.tab_1 import Tab_company
from utility.report import Pdf_Report,xlsx_Report
import time

Builder.load_file(os.path.join(os.path.dirname(__file__),f'report_scr.kv'))
class Nav_report_scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.nav_manager = ObjectProperty()
        lis=[('No.', dp(20)),("IO", dp(20)),("Style", dp(20)),("Color", dp(20)),("PO Qty", dp(20)),("Delivery Qty", dp(20)),("USD", dp(20)),("PO Value USD", dp(30)),("Delivery USD", dp(30)),("Excess Stock", dp(20)),("Stock Value USD", dp(30)),("Inr", dp(20)),("Percent", dp(20))]
        self.report=ClientsTable(list_col=lis,pageing=True)
        self.from_date=None
        self.to_date=None
        self.page_size = 100
        self.current_page = 0
        self.menu_page_size = 50
        self.menu_current_page = 0
        self.print_data=None
    def on_kv_post(self, base_widget):
        self.ids.report_table.add_widget(self.report)
    def on_enter(self, *args):
        Clock.schedule_once(self.load_report,0.5)
        # Clock.schedule_once(self.io_menu_fun, 1)
        # Clock.schedule_once(self.stye_menu_fun, 1.1)
        # Clock.schedule_once(self.color_menu_fun, 1.2)
        # Clock.schedule_once(self.pi_menu_fun, 1.3)
    def on_leave(self, *args):
        pass
    def load_report(self,*args):
        if self.app.admob:
            from utility.ad.my_ids import user_ids
            self.app.admob.load_banner(user_ids.BANNER, top=True)
        self.data=select_all(document)
        Clock.schedule_once(self.document_list, 0.1)
    def document_list(self,*args):
        self.report.data_tables.row_data=[ 
            (i.id,i.io,i.style,i.color,i.po_qty,i.delivery_qty,i.usd,i.po_value_usd,i.delivery_usd,i.excess_stock,i.stock_value_usd,i.inr,i.percent) for i in self.data
        ]
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
            data=[{'text':x.io,'on_press':partial(self.load_item_text_box,'io',x.io)} for x in self.data]
            Clock.schedule_once(partial(self.menu_update_page,'io',data),0.5)
        elif args[0]=='style':
            data=[{'text':x.style,'on_press':partial(self.load_item_text_box,'style',x.style)} for x in self.data]
            Clock.schedule_once(partial(self.menu_update_page,'style',data),0.5)
        elif args[0]=='color':
            data=[{'text':x.color,'on_press':partial(self.load_item_text_box,'color',x.color)} for x in self.data]
            Clock.schedule_once(partial(self.menu_update_page,'color',data),0.5) 
        elif args[0]=='pi':
            data=[{'text':x.pi,'on_press':partial(self.load_item_text_box,'pi',x.pi)} for x in self.data]
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
        data=[{'text':x.io,'on_press':partial(self.load_item_text_box,'io',x.io)} for x in self.data if x.io.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)
    def search_style_fun(self,*args):
        self.app.show_menu.content_cls.load_spinner=True
        self.txt=args[0]
        data=[{'text':x.style,'on_press':partial(self.load_item_text_box,'style',x.style)} for x in self.data if x.style.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)
    def search_color_fun(self,*args):
        self.app.show_menu.content_cls.load_spinner=True
        self.txt=args[0]
        data=[{'text':x.color,'on_press':partial(self.load_item_text_box,'color',x.color)} for x in self.data if x.color.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)
    def search_pi_fun(self,*args):
        self.app.show_menu.content_cls.load_spinner=True
        self.txt=args[0]
        data=[{'text':x.pi,'on_press':partial(self.load_item_text_box,'pi',x.pi)} for x in self.data if x.pi.lower().find(self.txt.lower())!=-1]
        if not self.txt:
            Clock.schedule_once(partial(self.menu_update_page,'no data',data),0.5)
            self.app.show_menu.content_cls.load_spinner=False
            return
        Clock.schedule_once(partial(self.menu_update_page,'search',data),0.5)

   
   
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
        data=[
        (i.id,i.io,i.style,i.color,i.po_qty,i.delivery_qty,i.usd,i.po_value_usd,i.delivery_usd,i.excess_stock,i.stock_value_usd,i.inr,i.percent) for i in search_data
        ]
        self.report.data_tables.row_data = data
        self.print_data=search_data
    def apply_filters(self, item, filters):
        date_filter = filters['date']
        if date_filter[0] and date_filter[1]:
            if not (date_filter[0] <= item.date.date() <= date_filter[1]):
                return False
        io_filter = filters['io']
        if io_filter and io_filter not in item.io:
            return False
        style_filter = filters['style']
        if style_filter and style_filter not in item.style:
            return False
        color_filter = filters['color']
        if color_filter and color_filter not in item.color:
            return False
        pi_filter = filters['pi']
        if pi_filter and pi_filter not in item.pi:
            return False
        search_filter = filters['search']
        if search_filter and (search_filter not in item.name and search_filter not in item.description):
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
        Clock.schedule_once(self.document_list, 1)
    def export_fun(self,*args):
        self.ids.print_btn.disabled=True
        self.ids.spin.active=True
        if self.app.alert_dialog:
            self.app.on_alret_dismiss()
        xl=xlsx_Report()
        hedaer_text=f'Doucment Report'
        footer_text=f'Powered By {self.app.company_name}'
        
        table_data=[["No.","IO","Style","Color","PO Qty","Delivery Qty","USD","PO Value USD","Delivery USD","Excess Stock","Stock Value USD","Inr","Percent"]]
        if not self.print_data:
            self.print_data=self.data
        for i in self.print_data:
            table_data.append([i.id,i.io,i.style,i.color,i.po_qty,i.delivery_qty,i.usd,i.po_value_usd,i.delivery_usd,i.excess_stock,i.stock_value_usd,i.inr,i.percent])
        time.sleep(1)
        files=f'report.xlsx'
        xl.xlsx(files,table_data,hedaer_text,footer_text)
        Clock.schedule_once(partial(self.app.notify,f'report save success'),1)
        Clock.schedule_once(partial(self.app.excute_fun,files),2)
        self.ids.print_btn.disabled=False
        self.ids.spin.active=False
