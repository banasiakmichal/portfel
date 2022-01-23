from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
import time
Window.size = (375, 667)

#todo: icon color - change!!!
kv = '''

#:import Factory kivy.factory.Factory

<MinusButton@MDIconButton>:
    icon: "minus-circle-outline"
    icon_size: "44sp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}

<Screen1>:
    text: input.text
    MDBoxLayout:
        # size_hint_y: 1
        orientation: 'vertical'
        spacing: 20
        padding: 20
    
        MDSeparator:
            height: "1dp"
            
        MDTextField:
            id: input
            heigh: '45dp'
            hint_text: "wpisz kwotę "
            mode: "fill"
            on_focus: self.text = ""
            #on_text:
                #root.add_input_items(cost_input.text)
                #root.validate_input(cost_input.text)
     
        MDSeparator:
            height: "1dp"
        
        MDLabel:
            size_hint_y: 0.1
            text: input.text
            halign: 'center'
            font_style: 'Body1'
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
                
        MDRaisedButton:
            text: 'print text from input'
            on_release:
                root.print_input()
                root.ids.input.text = ''
                    
        MinusButton:
            text: 'clear input'
            on_release:
                Factory.Screen1().pr(input.text)
                Factory.Screen1().clear()
                
'''


class Screen1(MDBottomNavigationItem):
    text = StringProperty()

    def print_input(self):
        print('property is:', self.text)

    def pr(self, text):
        print('property is:', text)

    def clear(self):
        self.text = ''
        self.ids.input.text = ''


class InfoDialog(MDDialog):
    dialog = None

    #def __init__(self, text):
        #self.text = text

    def dialog_(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                text=' ',
                radius=[20, 7, 20, 7],
            )
        self.dialog.open()

    def close(self):
        clo = lambda x: self.dialog.dismiss()
        #self.dialog.dismiss()


class MyApp(MDApp):

    dialog = None
    costs = '1000'

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        #self.theme_cls.primary_hue = "200"

        return Builder.load_string(kv)

    def on_start(self):
        self.dialog_close()

    def dialog_close(self):
        a = InfoDialog(text='some text').dialog_()
        time.sleep(1)
        # a.close()


MyApp().run()
