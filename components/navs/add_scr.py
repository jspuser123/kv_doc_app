from kivy.uix.screenmanager import Screen
from components.wgt import MDApp,Builder,Clock,partial,ObjectProperty,platform,os,shutil,Items_Card,Animation,ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget,MDDropdownMenu,filechooser
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
        directory, filename = os.path.split(path)
        self.ids.list_cards.add_widget(ThreeLineAvatarIconListItem(
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
                                                                secondary_text=filename,
                                                                tertiary_text= path,
                                                                ))
        self.ids.document_path.text=''
    def remove_document(self,item):
        for i in self.ids.list_cards.children:
            if i.id==item.id:
                self.ids.list_cards.remove_widget(i)
        print('remove',item.id)
    def save_document(self,*args):
        self.ids.spin.acitve=True
        name=self.ids.name.text
        description=self.ids.document_description.text
        io=self.ids.document_io.text
        style=self.ids.document_style.text
        color=self.ids.document_color.text
        pi=self.ids.document_pi.text
        po_qty= self.ids.po_qty.text if self.ids.po_qty.text else 0.0
        delivery_qty= self.ids.delivery_qty.text if self.ids.delivery_qty.text else 0.0
        usd= self.ids.usd.text if self.ids.usd.text else 0.0
        inr= self.ids.inr.text if self.ids.inr.text else 0.0
        excange_rate= self.ids.excange_rate.text if self.ids.excange_rate.text else 0.0
        po_value_usd= self.ids.po_value_usd.text if self.ids.po_value_usd.text else 0.0
        delivery_usd= self.ids.delivery_usd.text if self.ids.delivery_usd.text else 0.0
        excess_stock= self.ids.excess_shortage.text if self.ids.excess_shortage.text else 0.0
        percent= self.ids.percent.text if self.ids.percent.text else 0.0
        value= self.ids.document_value.text if self.ids.document_value.text else 0.0
        if not io:
            self.app.notify(f'please Add io',1)
            return
        try:
            with get_session() as session:
                x=document(name=name,description=description,io=io,style=style,color=color,pi=pi,value=value,date=datetime.now(),po_qty=float(po_qty),delivery_qty=float(delivery_qty),usd=float(usd),inr=float(inr),excange_rate=float(excange_rate),po_value_usd=float(po_value_usd),delivery_usd=float(delivery_usd),excess_stock=float(excess_stock),percent=float(percent))
                session.add(x)
                session.commit()
                self.doc_temp_id=x.id
                for i in self.ids.list_cards.children:
                    directory, filename = os.path.split(i.secondary_text)
                    img_name, extension = os.path.splitext(filename)
                    if not os.path.exists(f'{self.sys_path_year}/{i.text}'):os.mkdir(f'{self.sys_path_year}/{i.text}')
                    output=f'{self.sys_path_year}/{i.text}/{x.id}_{filename}{extension}'
                    shutil.copy(i.secondary_text, output)
                    insert_row(document_child,name=i.text,filename=filename,file=output,document_id=x.id)
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
                self.ids.documents_cards.add_widget(ThreeLineAvatarIconListItem(
                                                                        IconLeftWidget(
                                                                            icon="database"
                                                                        ),
                                                                        IconRightWidget(
                                                                            icon="arrow-right",
                                                                            on_release=partial(self.document_load,i.document_id,i.name,i.file),
                                                                        ),
                                                                        
                                                                        id=str(i.document_id),
                                                                        text=i.name,
                                                                        secondary_text=i.filename,
                                                                        tertiary_text=i.file,
                                                                        ))
        self.ids.spin.acitve=False
    def document_load(self,*args):
        id=args[0]
        name=args[1]
        link=args[2] 
        os.startfile(r'file:///'+link)
    def document_delete(self,*args):
        self.ids.spin.acitve=True
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
        self.ids.spin.acitve=False
    def cancel_document(self,*args):
        for k,v in self.ids.items():
            if k in ['list_cards','documents_cards','submit_btn','update_btn','cancel_btn']:
                continue
            v.text=''
        self.ids.list_cards.clear_widgets()
        self.ids.documents_cards.clear_widgets()
        self.ids.submit_btn.disabled=False
        self.ids.update_btn.disabled=True
        # self.nav_manager.current='nav_tab1'
    def document_menu(self,*args):
        menu_items = [
            {
                "text": f"{i.name}",
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
        self.ids.spin.acitve=True
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
                self.ids.documents_cards.add_widget(ThreeLineAvatarIconListItem(
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
                                                                        secondary_text=i.filename,
                                                                        tertiary_text=i.file,
                                                                        ))
        self.ids.name.text=data.name
        self.ids.document_description.text=data.desc
        self.ids.document_io.text=data.io
        self.ids.document_style.text=data.style
        self.ids.document_color.text=data.color
        self.ids.document_pi.text=data.pi
        ex_data=select_one(document,id=data.id_data)
        self.ids.excange_rate.text=str(ex_data.excange_rate)
        self.ids.po_qty.text=str(ex_data.po_qty)
        self.ids.delivery_qty.text=str(ex_data.delivery_qty)
        self.ids.usd.text=str(ex_data.usd)
        self.ids.po_value_usd.text=str(ex_data.po_value_usd)
        self.ids.delivery_usd.text=str(ex_data.delivery_usd)
        self.ids.excess_shortage.text=str(ex_data.excess_stock)
        self.ids.inr.text=str(ex_data.inr)
        self.ids.percent.text=str(ex_data.percent)
        self.ids.document_value.text=ex_data.value
        self.ids.spin.acitve=False
    def update_remove_document(self,*args):
        self.ids.spin.acitve=True
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
        self.ids.spin.acitve=False
    def document_update(self,*args):
        self.ids.spin.acitve=True
        if not self.ids.documents_cards.children:
            self.app.notify(f'No Update previes data',1)
            return
        id=self.ids.documents_cards.children[::-1][0].id_data
        name=self.ids.name.text
        description=self.ids.document_description.text
        io=self.ids.document_io.text
        style=self.ids.document_style.text
        color=self.ids.document_color.text
        pi=self.ids.document_pi.text
        po_qty= self.ids.po_qty.text if self.ids.po_qty.text else 0.0
        delivery_qty= self.ids.delivery_qty.text if self.ids.delivery_qty.text else 0.0
        usd= self.ids.usd.text if self.ids.usd.text else 0.0
        inr= self.ids.inr.text if self.ids.inr.text else 0.0
        excange_rate= self.ids.excange_rate.text if self.ids.excange_rate.text else 0.0
        po_value_usd= self.ids.po_value_usd.text if self.ids.po_value_usd.text else 0.0
        delivery_usd= self.ids.delivery_usd.text if self.ids.delivery_usd.text else 0.0
        excess_shortage= self.ids.excess_shortage.text if self.ids.excess_shortage.text else 0.0
        percent= self.ids.percent.text if self.ids.percent.text else 0.0
        value= self.ids.document_value.text if self.ids.document_value.text else 0.0
        if not io:
            self.app.notify(f'please Add io',1)
            return
        data={
            'name':name,
            'description':description,
            'io':io,
            'style':style,
            'color':color,
            'pi':pi,
            'po_qty':float(po_qty),
            'delivery_qty':float(delivery_qty),
            'usd':float(usd),
            'po_value_usd':float(po_value_usd),
            'delivery_usd':float(delivery_usd),
            'excange_rate':float(excange_rate),
            'excess_stock':float(excess_shortage),
            'inr':float(inr),
            'percent':float(percent),
            'value':value,
        
        }
        update_row(document,{'id':id},data)
        if self.ids.list_cards.children:
            try:
                for i in self.ids.list_cards.children:
                    directory, filename = os.path.split(i.secondary_text)
                    img_name, extension = os.path.splitext(filename)
                    if not os.path.exists(f'{self.sys_path_year}/{i.text}'):os.mkdir(f'{self.sys_path_year}/{i.text}')
                    output=f'{self.sys_path_year}/{i.text}/{id}_{filename}{extension}'
                    shutil.copy(i.secondary_text, output)
                    insert_row(document_child,name=i.text,filename=filename,file=output,document_id=id)
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
                self.ids.documents_cards.add_widget(ThreeLineAvatarIconListItem(
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
                                                                        secondary_text=i.filename,
                                                                        tertiary_text=i.file,
                                                                        ))
        self.ids.name.text=data['name']
        self.ids.document_description.text=data['description']
        self.ids.document_io.text=data['io']
        self.ids.document_style.text=data['style']
        self.ids.document_color.text=data['color']
        self.ids.document_pi.text=data['pi']
        self.ids.document_value.text=data['value']
        self.ids.spin.acitve=False
    def usd_calc(self,*args):
        try:
            if not args[0]:
                self.ids.po_value_usd.text=''
                self.ids.delivery_usd.text=''
                self.ids.excess_shortage.text=''
                self.ids.percent.text=''
                self.ids.document_value.text=''
                return
            po_qty= self.ids.po_qty.text if self.ids.po_qty.text else 0.0
            delivery_qty=self.ids.delivery_qty.text if self.ids.delivery_qty.text else 0.0
            usd=self.ids.usd.text
            inr=self.ids.inr.text
            if not inr and not usd:
                Clock.schedule_once(partial(self.app.notify,f'Inr and Usd not Value '),1)
            elif not usd or usd=='0.0' or usd=='0':
                po_value=float(po_qty)*float(inr)
                delivery_value=float(delivery_qty)*float(inr)
                self.ids.po_value_usd.text=f'{po_value:.2f}'
                self.ids.delivery_usd.text=f'{delivery_value:.2f}'
            elif not inr or inr=='0.0' or inr=='0':
                po_value=float(po_qty)*float(usd)*float(args[0])
                delivery_value=float(delivery_qty)*float(usd)*float(args[0])
                self.ids.po_value_usd.text=f'{po_value:.2f}'
                self.ids.delivery_usd.text=f'{delivery_value:.2f}'
            else:
                Clock.schedule_once(partial(self.app.notify,f'po value and delivery value not calculated '),1)
            excess_shortage=float(delivery_qty)-float(po_qty)
            self.ids.excess_shortage.text=f'{excess_shortage:.0f}'
            Clock.schedule_once(partial(self.inr_value_calc,args[0]),0.5)
        except Exception as e:
            Clock.schedule_once(partial(self.app.notify,f'usd_calc error:{e} '),1)

    def inr_value_calc(self,*args):
        try:
            if not args[0]:
                self.ids.document_value.text='0'
                return
            delivery_usd=self.ids.delivery_usd.text if self.ids.delivery_usd.text else 0.0
            excess_shortage=self.ids.excess_shortage.text if self.ids.excess_shortage.text else 0.0
            po_qty=self.ids.po_qty.text if self.ids.po_qty.text else 0.0
            percent=(float(excess_shortage)/float(po_qty))*100
            value=float(delivery_usd)*1.05
            self.ids.percent.text=f'{percent:.0f}'
            self.ids.document_value.text=f'{value:.2f}'
        except Exception as e:
            Clock.schedule_once(partial(self.app.notify,f'Percent error in inr_value_calc{e} '),1)
         
