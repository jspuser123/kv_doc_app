from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from components.wgt import MDDialog,MDFlatButton,DialogContent,Clock,platform,random,partial,sha256,math,datetime
from kivymd.uix.pickers import MDDatePicker
from screens.login import Login_page
from screens.regsistor import Regsistor_page
from screens.verfy import Verify_page
from screens.token_s import Token_page
from screens.forgot import Forgot_page 
from screens.home import HomeScreen
from kivymd.toast import toast
import smtplib
from PIL import ImageGrab

img = ImageGrab.grab()
img_size=img.size
size_display=(img_size[0]-30,img_size[1]-90)
Window.size = size_display
Window.top = 35
Window.left = 10
def reSize(*args):
   Window.size = size_display
   return True
Window.bind(on_resize = reSize)
# t=Window.size = (400, 600)

class DocApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alert_dialog = None
        self.setting_dialog = None
        self.admob=None
        self.date_b=[]
    def build(self):
        self.sm=ScreenManager()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.primary_palette = "Teal"
        self.sm.add_widget(Login_page(name='login_scr'))
        self.sm.add_widget(Regsistor_page(name='reg_scr'))
        self.sm.add_widget(Verify_page(name='verify_scr'))
        self.sm.add_widget(Token_page(name='token_scr'))
        self.sm.add_widget(Forgot_page(name='forgot_scr'))
        self.sm.add_widget(HomeScreen(name='home_scr'))
        return self.sm
    def on_start(self):
        Clock.schedule_once(self.andriod_config_fun,0.5)
        Clock.schedule_once(self.date_init,0.5)
    def date_init(self,*args):
        self.date_dialog = MDDatePicker()
    def date_on_cancel(self, instance, value):
        pass
    def show_date_picker(self,*args):
        if self.date_b:
            self.date_dialog.unbind(on_save=self.date_b[0])
            self.date_b=[]
        self.date_dialog.bind(on_save=args[0], on_cancel=self.date_on_cancel)
        self.date_dialog.open()
        self.date_b.append(args[0])
    def andriod_config_fun(self,*args):
        if platform == 'android':
            from utility.ad.admob4kivy import AdmobManager,TestIDs
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,Permission.RECORD_AUDIO,Permission.ACCESS_NETWORK_STATE])
            Window.keyboard_anim_args={'d':.2,'t':'in_out_expo'}
            Window.softinput_mode="below_target"
            self.admob = AdmobManager(callback=self.ad_event_callback)
    def show_alert_dialog(self,*args):
        self.alert_dialog = MDDialog(
            text=args[1] if len(args)>1 else "Are you Sure?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=self.on_alret_dismiss,
                ),
                MDFlatButton(
                    text="SAVE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=args[0],
                ),
            ],
        )
        self.alert_dialog.open()
    def show_setting_dialog(self,*args):
        self.setting_dialog = MDDialog(
            title="Add Ai Model:",
            type="custom",
            size_hint=(0.9, 0.9),
            content_cls=DialogContent(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=self.on_dismiss,
                ),
                MDFlatButton(
                    text="Submit",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=args[0],
                ),
            ],
        )
        self.setting_dialog.open()
    def notify(self,text:str,*args):
        toast(text)
    def on_alret_dismiss(self,*args):
        self.alert_dialog.dismiss()
    def on_dismiss(self,*args):
        self.setting_dialog.dismiss()
    def id_gen(self,*args):
        digits="0123456789"
        OTP=''
        for i in range(10):
            OTP+=digits[math.floor(random.random()*10)]
        return OTP
    def otp_gen(self,*args):
        digits="0123456789"
        OTP=''
        for i in range(4):
            OTP+=digits[math.floor(random.random()*10)]
        return OTP
    def send_email(self,eml,msg):
        try:
            s = smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login("asp6406@gmail.com", "eysa ffxe otzf qewk")
            s.sendmail('no-reply',eml,msg)
            s.close()
        except:
            Clock.schedule_once(partial(self.notify,f'email not send some_error'),1)
    def token_gen(self,*args):
        try:
            company=args[0]
            t=datetime.now()
            ins=f'{company}:{t.year}asp@321'
            self.token=sha256(ins.encode('utf-8')).hexdigest()
        except Exception as e:
            self.noty_fy(f'token error{e}') 
    def ad_event_callback(self, event, *args):  ####this ad related function is not working
        print(f"[AdEvent in Kivy APP ] {event}: {args}")
    def on_exit(self,*args):
        self.stop()
if __name__ == '__main__':
    DocApp().run()