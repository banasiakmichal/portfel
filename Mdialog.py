from kivymd.uix.dialog import MDDialog


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
