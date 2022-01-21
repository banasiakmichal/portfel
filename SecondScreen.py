from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.app import App
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
from storage import store
from kivy.uix.recycleview import RecycleView
from kivy.properties import NumericProperty, StringProperty
# costs = {'van': 5500, 'marzec': 4000}


class SecondScreen(MDBottomNavigationItem):
    pass


class CostsView(RecycleView):
    """ RV for Projects """

    def __init__(self, **kwargs):
        super(CostsView, self).__init__(**kwargs)
        Clock.schedule_once(self.populate_view)

    def populate_view(self, *args):
        if store['costs']:
            try:
                self.data = [{'text': f"{key} :  {value} zł"} for key, value in store['costs'].items()]
            except Exception as e:
                print('found exception in CatView')
                # todo: connect this to logger module
        else:
            self.data = []
        return self.data
