from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os,ClientsTable,dp
from models.model import document_name,document,document_child,path_server
from models.db_con import *
# from components.tabs.add.tab_1 import Tab_company

Builder.load_file(os.path.join(os.path.dirname(__file__),f'report_scr.kv'))
class Nav_report_scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.nav_manager = ObjectProperty()
        lis=[('No.', dp(20)),("IO", dp(20)),("Style", dp(20)),("Color", dp(20)),("PO Qty", dp(20)),("Delivery Qty", dp(20)),("USD", dp(20)),("PO Value USD", dp(30)),("Delivery USD", dp(20)),("Excess Stock", dp(20)),("Stock Value USD", dp(30)),("Inr", dp(20)),("Percent", dp(20))]
        self.report=ClientsTable(list_col=lis,pageing=True)
    def on_kv_post(self, base_widget):
        self.ids.report_table.add_widget(self.report)
    def on_enter(self, *args):
        Clock.schedule_once(self.load_report,1)
    def on_leave(self, *args):
        pass
    def load_report(self,*args):
        self.data=select_all(document)
        self.report.data_tables.row_data=[ 
            (i.id,i.io,i.style,i.color,i.po_qty,i.delivery_qty,i.usd,i.po_value_usd,i.delivery_usd,i.excess_stock,i.stock_value_usd,i.inr,i.percent) for i in self.data
        ]