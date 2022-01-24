from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.clock import Clock
from storage import store
from kivy.uix.recycleview import RecycleView
from Mdialog import InfoDialog


class SecondScreen(MDBottomNavigationItem):
    pass


class GeneralView(RecycleView):
    """ RV costs in time"""
    def __init__(self, **kwargs):
        super(GeneralView, self).__init__(**kwargs)
        Clock.schedule_once(self.populate_view)

    def populate_view(self, *args):
        if store['costs']:
            try:
                self.data = [{'text': f"{k} :  {v} zł"} for k, v in store['costs'].items() if k != 'RAZEM']
            except Exception as e:
                self.data = []   #todo: v.2 - logging module with e, emialclient, internet permission
                InfoDialog(text='UPSS...coś poszło nie tak. Wykonaj restart aplikacji').dialog_()
        else:
            self.data = []
        return self.data


class CostsView(RecycleView):
    """ RV for cat and pro costs """
    def __init__(self, **kwargs):
        super(CostsView, self).__init__(**kwargs)
        Clock.schedule_once(self.populate_view)

    def populate_view(self, *args):
        if store['catpro']:
            try:
                self.data = [{'text': f"{k.upper()} : {v[0]} zł",
                              'secondary_text': f"w tym tygodniu: {v[1]} zł",
                              'tertiary_text': f"w tym miesiącu: {v[2]} zł"} for k, v in store['catpro'].items()]
            except Exception as e:
                self.data = []  #todo: v.2 - logging module with e, emialclient, internet permission
                InfoDialog(text='UPSS...coś poszło nie tak. Wykonaj restart aplikacji').dialog_()
        else:
            self.data = []
        return self.data


