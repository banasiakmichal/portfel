from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

""" PopUp dialog window 
import ...
  use in class attr: dialog = None
     call: Dialog(text)_dialog_(self) """


class MyDialog(MDDialog, MDFlatButton):
    dialog = None

    def __init__(self, text):
        self.text = text

    def dialog_(self, *args):
        if not self.dialog:
             self.dialog = MDDialog(
                size_hint_x=0.8,
                text=self.text,
                buttons=[
                    MDFlatButton(
                        text="ZAMKNIJ OKNO", theme_text_color="Custom", text_color=(0.902, 0.494, 0.133, 1),
                        on_release=lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()


class InfoDialog(MDDialog):
    dialog = None

    def __init__(self, text):
        self.text = text

    def dialog_(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                text=self.text,
                radius=[20, 7, 20, 7],
            )
        self.dialog.open()
