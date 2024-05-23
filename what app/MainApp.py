import os
from kivy.properties import ObjectProperty ,StringProperty,BooleanProperty,NumericProperty,DictProperty
from kivy.lang import Builder
from kivy.base import EventLoop
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.metrics import dp as sdp
from kivy.uix.button import Button
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.chip import MDChip, MDChipText,MDChipLeadingIcon
from kivymd.uix.card import MDCard
#from kivymd.uix.dialog import BaseDialog
from functools import partial

## ADD  IF YOU ARE RUNNING CODE FROM Parent Directory 


from data import data, dirname as path_ui


#My This module we are not using here 
#from .mymodalview import MyModalView

import asynckivy


path =os.getcwd()
## what's app clone 

#Builder.load_file(os.path.join(os.getcwd(),"ui1.kv"))
Builder.load_file(os.path.join(path_ui,"ui1.kv"))

class UI1Dialog(ModalView):
    _name=StringProperty('')
    _dp=StringProperty('')
    _radius=NumericProperty(0)
    def on_dismiss(self,*a):
        self.size_hint=(0,0)
        self._radius=sdp(50)

class UI1NavigationBar(MDNavigationBar):
    obj=ObjectProperty(None)
    def on_switch_tabs(self,*args):
        item_text=args[-1]
        item_icon=args[-2]
        if item_text=='Chats':

            self.obj.ids.screen_manager.current='chatscreen'
        if item_text=='Updates':
            self.obj.ids.screen_manager.current='updatesscreen'
        if item_text=='Communities':
            self.obj.ids.screen_manager.current='communitiesscreen'
        if item_text=='Calls':
            self.obj.ids.screen_manager.current='callscreen'


        
        #print(item_text,item_icon)
    def _on_active(self,*args):pass
        # for i in args[0].children:
        #     print(i)

class UI1TextField(TextInput):pass
class UI1SearchPlate(MDBoxLayout):
    obj=ObjectProperty(None)
    obj2=ObjectProperty(None)
    
    index=NumericProperty(None)
    def on_kv_post(self,obj):
        asynckivy.start(self.create_chips())
        #self.create_chips()
        print("hello")
    def _focus(self,obj,focus):
        if focus:
            print("focus")
        else:
            print("not focuas")
            self.obj.ids.scroll_box.remove_widget(self)
            self.obj.ids.scroll_box.add_widget(self.obj2,index=int(self.index))



    async def create_chips(self):
        '''Asynchronously creates and adds chips to the container.'''
        tags=["Unread", "Photos", "Videos", "Links","GIFs","Audio","Documents","Polls"]
        icons=["message-bulleted","image-outline","video-outline","link","file-gif-box","headphones","file-document","poll"]
        for tag,icon in zip(tags,icons) :
            await asynckivy.sleep(0)
            self.ids.stack_box.add_widget(
                MDChip(
                    MDChipLeadingIcon(icon=icon),
                    MDChipText(
                        text=tag,),

                    type="filter",
                    md_bg_color="#303A29",
                    
                    active=True,
                )
            )

class UI1ChatLabel(MDLabel):
    sender=BooleanProperty(True)
    def on_kv_post(self,obj):
        if self.sender:
            self.pos_hint={'right':1}
        else:
            self.pos_hint={'x':0}


class UI1Item(MDListItem):
    obj=ObjectProperty(None)
    dp_pic=StringProperty(os.path.join(path_ui,'res',"i1.jpg"))
    name=StringProperty("Emma")
    last_message=StringProperty("Hi !")
    dialog=None
    
    def _open_dialog(self,dpic,name,*args):
        #We can try to do UI1Dialog start grow from that widget and it move another position 
        #But ModalView has some limitations 
        #I Will try latter .
        # So a widget start grow from touch point and move to another position 
        #You can try . To implement that type of animation 
        if not self.dialog:
            self.dialog=UI1Dialog(size_hint=(0,0),_radius=50,pos_hint={'center_x':0.5,'center_y':0.6})
        self.dialog._name=name
        self.dialog._dp=dpic
        self.dialog.open()
        anim=Animation(size_hint=(0.8,0.45))
        anim&=Animation(_radius=0,d=5)
        anim.start(self.dialog)
        


        
        
        #print(dpic,name)
class UI1ChatScreen(MDScreen):
    obj=ObjectProperty(None)
    chat_name=StringProperty("name")
    dp_pic=StringProperty("")
    nav_bar=ObjectProperty(None)
    chats=DictProperty({})
    #chat_screen_object=None
    _ak=None
    def on_enter(self):
        print("hello")
        Window.softinput_mode = 'below_target'
        self._ak=asynckivy.start(self.load_chats())
    def _focus(self,*args):pass
        # print("ehllo")
        # state=args[1]
        # Window.softinput_mode = 'below_target' if state else ''
        # print(Window.softinput_mode)
    
    def on_leave(self):
        #self.chats={}
        Window.softinput_mode = ''
        print("hello leave ###"*100)
        self._ak.cancel()
        self.ids.chat_box.clear_widgets()
        self.obj.ids.box0.add_widget(self.nav_bar)

    
    async def load_chats(self):
        for i,j in zip(self.chats['there'],self.chats['here']):

            self.ids.chat_box.add_widget(UI1ChatLabel(sender=True,text=i))
            await asynckivy.sleep(0.5)
            last=UI1ChatLabel(sender=False,text=j)
            self.ids.chat_box.add_widget(last)
            ## to scroll new messages
            self.ids.chat_box.parent.scroll_y=0
            await asynckivy.sleep(0.5)
        
        




    
    


    def on_pre_enter(self):
        EventLoop.window.bind(on_keyboard=self._android_back_click)
    def on_pre_leave(self):
        EventLoop.window.unbind(on_keyboard=self._android_back_click)
    def _android_back_click(self,window,key,*largs):
        if key == 27:
            #print(self.obj.ids.screen_manager.screen_names)
            #print("hhhh")
            #print(self.obj.ids.screen_manager2.current)

            if self.obj.ids.screen_manager.current=='ui1chatscreen':
                self.obj.ids.screen_manager.current='chatscreen'
            
            return True


class UI1UpdatesScreen(MDScreen):
    _a=None

    def on_kv_post(self,obj):
        # Here I have used asynckivy to see the beauty of Async kivy 
        #asynckivy.sleep(0.5) you can change value 0.5.
        pass
    def on_enter(self):
        #In WhatsApp Widget Creation not like that but i  have implemented to see the beauty 
        #of asynckivy  
        self._a=asynckivy.start(self._init())
    
    async def _init(self):

        for i in data:
            name,dp,ct,ch,chats=i['name'],i['dp'],i['chats']['there'],i['chats']['here'],i['chats']
            dp_path=os.path.join(path_ui,'res',dp)
            await asynckivy.sleep(0.2)
            #print("Helllo")
            self.ids.bfc.add_widget(UI1FollowCard(pic=dp_path,_name=name))
            self.ids.bss.add_widget(UI1Status(pic=dp_path,person_name=name))
    def on_leave(self):
        ## self._a.cancel() used to stop if any one leave screen during the object creation 
        self._a.cancel()
        self.ids.bss.clear_widgets()
        self.ids.bfc.clear_widgets()


    
    




class UI1Status(MDBoxLayout):
    pic=StringProperty(os.path.join(path_ui,'res',"i1.jpg"))
    person_name=StringProperty('My Status')
class UI1FollowCard(MDCard):
    pic=StringProperty("")
    _name=StringProperty("Unkonwn")

class UI1CommunitiesScreen(MDScreen):pass
class UI1CallsScreen(MDScreen):pass

class UI1Screen(MDScreen):
    obj=ObjectProperty(None)
    nav_bar=ObjectProperty(None)
    chat_screen_object=None
    def on_kv_post(self,obj):
        #Window.softinput_mode = 'below_target'
        for i in data:
            name,dp,ct,ch,chats=i['name'],i['dp'],i['chats']['there'],i['chats']['here'],i['chats']
            dp_path=os.path.join(path_ui,'res',dp)

            last_message= ct[-1] if len(ct)>len(ch) else ch[-1]
            self.ids.scroll_box.add_widget(UI1Item(obj=self,name=name,dp_pic=dp_path,\
                last_message=last_message,on_release=partial(self._open_chat,name,dp_path,chats)))
        self.nav_bar=UI1NavigationBar(obj=self)
        self.ids.box0.add_widget(self.nav_bar)
    
    


    def on_active(*args):pass
        #print(args)

    def _open_chat(self,name,dp_path,chats,obj):
        print(name,dp_path,chats,obj)

        if not self.ids.screen_manager.has_screen("ui1chatscreen"):
            self.chat_screen_object=UI1ChatScreen(obj=self)
            self.ids.screen_manager.add_widget(self.chat_screen_object)
        
        self.chat_screen_object.chat_name=name
        self.chat_screen_object.dp_pic=dp_path
        #self.chat_screen_object.chats={}
        self.chat_screen_object.chats=chats
        self.chat_screen_object.nav_bar=self.nav_bar
        self.ids.box0.remove_widget(self.nav_bar)
        self.ids.screen_manager.current='ui1chatscreen'








    def on_pre_enter(self):
        EventLoop.window.bind(on_keyboard=self._android_back_click)

    def on_pre_leave(self):
        EventLoop.window.unbind(on_keyboard=self._android_back_click)
    def go_back_mainscreen(self):
        print(self.obj)
        self.obj.ids.sm.current="s1"

    def _android_back_click(self,window,key,*largs):
        if key == 27:
            print(self.obj.ids.sm.screen_names)
            print(self.ids.screen_manager.screen_names)
            # if self.obj.ids.sm.current=="ui1screen":
            #     self.go_back_mainscreen()
                #EventLoop.window.unbind(on_keyboard=self._android_back_click)
            # if self.ids.screen_manager2.current=='ui1chatscreen':
            #     self.ids.screen_manager.current='chatscreen'
            #     return True


            if  self.ids.screen_manager.current=="chatscreen":
                self.obj.ids.sm.current="s1"
            if self.ids.screen_manager.current=="updatesscreen" or "communitiesscreen" or "callscreen" :
                self.ids.screen_manager.current="chatscreen"
            
                    

            
                #print("hello")
            return True
    def _search_button_clicked(self):
        print("Helllo")
        
        a=self.ids.scroll_box.children
        a=list(a)
        index=a.index(self.ids.box_as)
        print(index)
        obj2=self.ids.box_as
        self.ids.scroll_box.remove_widget(self.ids.box_as)
        self.ids.scroll_box.add_widget(UI1SearchPlate(obj=self,obj2=obj2,index=index),index=index)
    


class MainApp(MDApp):
    def build(self):
        
        return UI1Screen(obj=self)
    def on_start(self):
        super().on_start()
        #self.fps_monitor_start()
if __name__ == '__main__':
    MainApp().run()
