from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.app import App
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
from storage import store
from kivy.uix.recycleview import RecycleView
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.list import OneLineListItem
# costs = {'van': 5500, 'marzec': 4000}


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
                # f k == 'dzisiaj' or k == 'w tym tygodniu' or k == 'w tym miesiącu' or k == 'w tym roku'
            except Exception as e:
                print('found exception in CatView')
                # todo: connect this to logger module
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
                self.data = [{'text': f"{k.upper()} : {v[0]} zł", 'secondary_text': f"w tym tygodniu: {v[1]}", 'tertiary_text': f"w tym miesiącu: {v[2]}"} for k, v in store['catpro'].items()]
            except Exception as e:
                print('found exception in CatView')
                # todo: connect this to logger module
        else:
            self.data = []
        return self.data


