from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os,shutil,Items_Card,Animation,TwoLineAvatarIconListItem,IconLeftWidget,IconRightWidget,MDDropdownMenu,filechooser
from models.model import document_name,document,document_child,path_server
from models.db_con import *
# from components.tabs.add.tab_1 import Tab_company

Builder.load_file(os.path.join(os.path.dirname(__file__),f'add_scr.kv'))
class Nav_add_scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.nav_manager = ObjectProperty()
    def on_enter(self, *args):
        Clock.schedule_once(self.document_menu,1)
        Clock.schedule_once(self.path_load,1)
    def on_leave(self, *args):
        pass
    def path_load(self,*args):
        try:
            x=select_one(path_server,id=1)
            self.system_path=x.path if x else ''
            self.sys_path_year=''
            if self.system_path:
                self.year=datetime.now().year
                self.sys_path_year=f'{self.system_path}/{self.year}'
                if not os.path.exists(self.sys_path_year):os.mkdir(f'{self.sys_path_year}')
            else:
                self.app.notify(f'Error: Unable to server path {self.system_path}')
        except FileNotFoundError:
            self.app.notify(f'Error: Unable to create directory {self.system_path}')
    def upload_document(self,*args):
        self.doc_id=self.app.id_gen()
        name=self.ids.document_name.text
        path=self.ids.document_path.text
        if not name and not path:
            return
        self.ids.list_cards.add_widget(TwoLineAvatarIconListItem(
                                                                IconLeftWidget(
                                                                    icon="database"
                                                                ),
                                                                IconRightWidget(
                                                                    id=self.doc_id,
                                                                    icon="close",
                                                                    on_release=self.remove_document,
                                                                ),
                                                                id=self.doc_id,
                                                                text=name,
                                                                secondary_text=path,
                                                                ))
        self.ids.document_name.text=''
        self.ids.document_path.text=''
    def remove_document(self,item):
        for i in self.ids.list_cards.children:
            if i.id==item.id:
                self.ids.list_cards.remove_widget(i)
        print('remove',item.id)
    def save_document(self,*args):
        name=self.ids.name.text_in.text
        description=self.ids.document_description.text_in.text
        io=self.ids.document_io.text_in.text
        style=self.ids.document_style.text_in.text
        color=self.ids.document_color.text_in.text
        pi=self.ids.document_pi.text_in.text
        po_qty=self.ids.po_qty.text_in.text
        delivery_qty=self.ids.delivery_qty.text_in.text
        usd=self.ids.usd.text_in.text
        po_value_usd=self.ids.po_value_usd.text_in.text
        delivery_usd=self.ids.delivery_usd.text_in.text
        excess_stock=self.ids.excess_stock.text_in.text
        stock_value_usd=self.ids.stock_value_usd.text_in.text
        inr=self.ids.inr.text_in.text
        percent=self.ids.percent.text_in.text
        value=self.ids.document_value.text_in.text
        if not name and not description and not io and not style and not color and not pi and not value:
            return
        try:
            with get_session() as session:
                x=document(name=name,description=description,io=io,style=style,color=color,pi=pi,value=value,date=datetime.now(),po_qty=float(po_qty),delivery_qty=float(delivery_qty),usd=float(usd),po_value_usd=float(po_value_usd),delivery_usd=float(delivery_usd),excess_stock=float(excess_stock),stock_value_usd=float(stock_value_usd),inr=float(inr),percent=float(percent))
                session.add(x)
                session.commit()
                self.doc_temp_id=x.id
                for i in self.ids.list_cards.children:
                    directory, filename = os.path.split(i.secondary_text)
                    img_name, extension = os.path.splitext(filename)
                    if not os.path.exists(f'{self.sys_path_year}/{i.text}'):os.mkdir(f'{self.sys_path_year}/{i.text}')
                    id=self.app.id_gen()
                    output=f'{self.sys_path_year}/{i.text}/{x.id}_{id}{extension}'
                    shutil.copy(i.secondary_text, output)
                    insert_row(document_child,name=i.text,file=output,document_id=x.id)
        except Exception as e:
            self.app.notify(f'Error: {e}',1)
            return
        Clock.schedule_once(self.cancel_document,1)
        Clock.schedule_once(partial(self.app.notify,f'Document {name} saved'),1)
        Clock.schedule_once(self.temp_document,1)
       # self.nav_manager.current = "first_scr"
    def temp_document(self,*args):
        data=select_one(document,id=self.doc_temp_id)
        x=Items_Card()
        x.name=data.name
        x.desc=data.description
        x.io=data.io
        x.style=data.style
        x.color=data.color
        x.pi=data.pi
        x.value=data.value
        x.date=str(data.date.strftime('%Y-%m-%d'))
        x.id_data=data.id
        x.opacity=0
        self.ids.documents_cards.add_widget(x)
        Animation(opacity=1,d=.5,t='out_quad').start(x)
        x=select_all(document_child,document_id=self.doc_temp_id)
        if x:
            for i in x:
                self.ids.documents_cards.add_widget(TwoLineAvatarIconListItem(
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
        id=args[0]
        name=args[1]
        link=args[2] 
        os.startfile(r'file:///'+link)
    def document_delete(self,*args):
        try:
            x=args[0].id_data
            with get_session() as session:
                doc = session.query(document).get(x.id_data)
                for child in doc.document_child:
                    if os.path.exists(child.file):
                        os.remove(child.file)
                session.delete(doc)
                session.commit()
            Clock.schedule_once(self.nav_manager.get_screen('first_scr').document_list,1.2)
            self.ids.documents_cards.remove_widget(args[0])
        except Exception as e:
            self.app.notify(f'Error: {e}',1)
    def cancel_document(self,*args):
        self.ids.name.text_in.text=''
        self.ids.document_description.text_in.text=''
        self.ids.document_io.text_in.text=''
        self.ids.document_style.text_in.text=''
        self.ids.document_color.text_in.text=''
        self.ids.document_pi.text_in.text=''
        self.ids.document_value.text_in.text=''
        self.ids.document_name.text=''
        self.ids.document_path.text=''
        self.ids.po_qty.text_in.text=''
        self.ids.delivery_qty.text_in.text=''
        self.ids.usd.text_in.text=''
        self.ids.po_value_usd.text_in.text=''
        self.ids.delivery_usd.text_in.text=''
        self.ids.excess_stock.text_in.text=''
        self.ids.stock_value_usd.text_in.text=''
        self.ids.inr.text_in.text=''
        self.ids.percent.text_in.text=''
        self.ids.list_cards.clear_widgets()
        self.ids.documents_cards.clear_widgets()
        self.ids.submit_btn.disabled=False
        self.ids.update_btn.disabled=True
        # self.nav_manager.current='nav_tab1'
    def document_menu(self,*args):
        menu_items = [
            {
                "text": f"Item {i.name}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i.name: self.menu_callback(x),
            } for i in select_all(document_name)
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.document_name,
            background_color=self.app.theme_cls.primary_light,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        


    def menu_callback(self, text_item):
        self.ids.document_name.text=text_item
        self.menu.dismiss()
    def document_view(self,*args):
        path=filechooser.open_file(title="Select a file")
        if path:
            self.ids.document_path.text=str(path[0])
            Clock.schedule_once(partial(self.app.notify,f'Selected file(s): {path[0]}'),1)
        else:
            Clock.schedule_once(partial(self.app.notify,f'No file selected.'),1)
    def remove_item(self,item):
        self.ids.list_cards.remove_widget(item)
    def document_update_data(self,*args):
        self.ids.submit_btn.disabled=True
        self.ids.update_btn.disabled=False
        self.ids.documents_cards.clear_widgets()
        data=args[0]
        card=Items_Card()
        card.name=data.name
        card.desc=data.desc
        card.io=data.io
        card.style=data.style
        card.color=data.color
        card.pi=data.pi
        card.value=data.value
        card.date=data.date
        card.id_data=data.id_data
        card.opacity=0
        self.ids.documents_cards.add_widget(card)
        Animation(opacity=1,d=.5,t='out_quad').start(card)
        x=select_all(document_child,document_id=data.id_data)
        if x:
            for i in x:
                self.ids.documents_cards.add_widget(TwoLineAvatarIconListItem(
                                                                        IconLeftWidget(
                                                                            icon="database"
                                                                        ),
                                                                        IconRightWidget(
                                                                            id=str(i.document_id),
                                                                            icon="close",
                                                                            on_release=partial(self.update_remove_document,i.document_id,i.name,i.file),
                                                                        ),
                                                                        
                                                                        id=str(i.document_id),
                                                                        text=i.name,
                                                                        secondary_text=i.file,
                                                                        ))
        self.ids.name.text_in.text=data.name
        self.ids.document_description.text_in.text=data.desc
        self.ids.document_io.text_in.text=data.io
        self.ids.document_style.text_in.text=data.style
        self.ids.document_color.text_in.text=data.color
        self.ids.document_pi.text_in.text=data.pi
        ex_data=select_one(document,id=data.id_data)
        self.ids.po_qty.text_in.text=str(ex_data.po_qty)
        self.ids.delivery_qty.text_in.text=str(ex_data.delivery_qty)
        self.ids.usd.text_in.text=str(ex_data.usd)
        self.ids.po_value_usd.text_in.text=str(ex_data.po_value_usd)
        self.ids.delivery_usd.text_in.text=str(ex_data.delivery_usd)
        self.ids.excess_stock.text_in.text=str(ex_data.excess_stock)
        self.ids.stock_value_usd.text_in.text=str(ex_data.stock_value_usd)
        self.ids.inr.text_in.text=str(ex_data.inr)
        self.ids.percent.text_in.text=str(ex_data.percent)
        self.ids.document_value.text_in.text=ex_data.value

    def update_remove_document(self,*args):
        id=args[0]
        name=args[1]
        file=args[2]
        try:
            if os.path.exists(file):os.remove(file)
            delete_row(document_child,document_id=id)
            for i in self.ids.documents_cards.children:
                if i.id==str(id):
                    self.ids.documents_cards.remove_widget(i)
            print('remove',id)
        except Exception as e:
            self.app.notify(f'Error: {e}',1)
    def document_update(self,*args):
        if not self.ids.documents_cards.children:
            print('no document list')
            return
        id=self.ids.documents_cards.children[::-1][0].id_data
        name=self.ids.name.text_in.text
        description=self.ids.document_description.text_in.text
        io=self.ids.document_io.text_in.text
        style=self.ids.document_style.text_in.text
        color=self.ids.document_color.text_in.text
        pi=self.ids.document_pi.text_in.text
        po_qty=self.ids.po_qty.text_in.text
        delivery_qty=self.ids.delivery_qty.text_in.text
        usd=self.ids.usd.text_in.text
        po_value_usd=self.ids.po_value_usd.text_in.text
        delivery_usd=self.ids.delivery_usd.text_in.text
        excess_stock=self.ids.excess_stock.text_in.text
        stock_value_usd=self.ids.stock_value_usd.text_in.text
        inr=self.ids.inr.text_in.text
        percent=self.ids.percent.text_in.text
        value=self.ids.document_value.text_in.text
        if name and description and io and style and color and  pi and value:
            data={
                'name':name,
                'description':description,
                'io':io,
                'style':style,
                'color':color,
                'pi':pi,
                'value':value,
                'po_qty':float(po_qty),
                'delivery_qty':float(delivery_qty),
                'usd':float(usd),
                'po_value_usd':float(po_value_usd),
                'delivery_usd':float(delivery_usd),
                'excess_stock':float(excess_stock),
                'stock_value_usd':float(stock_value_usd),
                'inr':float(inr),
                'percent':float(percent),
            }
            update_row(document,{'id':id},data)
        if self.ids.list_cards.children:
            try:
                for i in self.ids.list_cards.children:
                    directory, filename = os.path.split(i.secondary_text)
                    img_name, extension = os.path.splitext(filename)
                    if not os.path.exists(f'{self.sys_path_year}/{i.text}'):os.mkdir(f'{self.sys_path_year}/{i.text}')
                    id_token=self.app.id_gen()
                    output=f'{self.sys_path_year}/{i.text}/{id}_{id_token}{extension}'
                    shutil.copy(i.secondary_text, output)
                    insert_row(document_child,name=i.text,file=output,document_id=id)
            except Exception as e:
                self.app.notify(f'Error: {e}',1)
                return
        self.ids.list_cards.clear_widgets()
        self.ids.documents_cards.clear_widgets()
        Clock.schedule_once(partial(self.document_update_data_view,id,data),1.2)
    def document_update_data_view(self,*args):###this change fun
        self.ids.documents_cards.clear_widgets()
        id=args[0]
        data=args[1]
        card=Items_Card()
        card.name=data['name']
        card.desc=data['description']
        card.io=data['io']
        card.style=data['style']
        card.color=data['color']
        card.pi=data['pi']
        card.value=data['value']
        card.date=datetime.now().strftime('%Y-%m-%d')
        card.id_data=id
        card.opacity=0
        self.ids.documents_cards.add_widget(card)
        Animation(opacity=1,d=.5,t='out_quad').start(card)
        x=select_all(document_child,document_id=id)
        if x:
            for i in x:
                self.ids.documents_cards.add_widget(TwoLineAvatarIconListItem(
                                                                        IconLeftWidget(
                                                                            icon="database"
                                                                        ),
                                                                        IconRightWidget(
                                                                            id=str(i.document_id),
                                                                            icon="close",
                                                                            on_release=partial(self.update_remove_document,i.document_id,i.name,i.file),
                                                                        ),
                                                                        
                                                                        id=str(i.document_id),
                                                                        text=i.name,
                                                                        secondary_text=i.file,
                                                                        ))
        self.ids.name.text_in.text=data['name']
        self.ids.document_description.text_in.text=data['description']
        self.ids.document_io.text_in.text=data['io']
        self.ids.document_style.text_in.text=data['style']
        self.ids.document_color.text_in.text=data['color']
        self.ids.document_pi.text_in.text=data['pi']
        self.ids.document_value.text_in.text=data['value']