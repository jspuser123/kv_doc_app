from components.wgt import MDApp ,Builder,Clock,partial,Tab,os

Builder.load_file(os.path.join(os.path.dirname(__file__),f'tab_1.kv'))
class Tab_company(Tab):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ins_row=None
        self.selected_check_box=[]
        self.current_tab=None
        self.app=MDApp.get_running_app()
        self.per_id=None