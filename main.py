"""  https://github.com/banasiakmichal/portfel.git """

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigation
import SecondScreen
import FirstScreen
import ThirdScreen
from class_mydb import Mydb
from storage import store
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial
Window.size = (375, 667)


class Manager(MDBottomNavigation):
    pass


kv = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:include FirstScreen.kv
#:include SecondScreen.kv
#:include ThirdScreen.kv

MDScreen:
    Manager:
        panel_color: get_color_from_hex("#eeeaea")
        selected_color_background: get_color_from_hex("#97ecf8")
        text_color_active: 0, 0, 0, 1

        FirstScreen:
            id: screen1
            name: 'screen1'
            text: 'Ogólne'
            icon: 'account-cash'
            # badge_icon: "numeric-10"
            on_leave:
                app.update_all()
                screen2.ids.costs_view.populate_view()


        SecondScreen:
            id: screen2
            name: 'screen2'
            text: 'Portfel'
            icon: 'format-list-bulleted-type'
            #on_leave:
                #self.all_costs()

        ThirdScreen:
            name: 'screen3'
            text: 'Ustawienia'
            icon: 'table-settings'
            on_leave:
                screen1.ids.cat_view.populate_view()
                screen1.ids.pro_view.populate_view()
'''


class Budget(MDApp):
    db = Mydb()

    def build(self):
        self.icon = 'logo.png'
        return Builder.load_string(kv)

    def on_start(self):
        """ update views from db """
        self.update_store_cat_pro('category', 'project')
        self.update_all()

    """ fetch db methods """
    def update_store_cat_pro(self, *args):
        for i in args:
            rows = self.db.fetch_col(i)
            items = [i for item in rows for i in item if i is not None]
            if i is 'category':
                store['category']['cat'] = list(dict.fromkeys(items))
            else:
                store['project']['pro'] = list(dict.fromkeys(items))

    def update_all(self):
        self.fetch_costs()
        self.fetch_today_cost()
        self.fetch_week_cost()
        self.fetch_c_month()
        self.fetch_l_month()
        self.fetch_year()
        self.fetch_l_year()
        Clock.schedule_once(partial(self.db.cat_pro_costs, 'category', store['category']['cat']))
        Clock.schedule_once(partial(self.db.cat_pro_costs, 'project', store['project']['pro']))

    def fetch_costs(self):
        """  all costs for pro, cat and datas source in mydb class"""
        #todo: def fetch costs fromdb check if smth changed and if True - update store['costs']
         #todo: if smth changed use new collor to show it !! important
        rows = self.db.fetch_col(col='cost')
        store['costs']['RAZEM'] = sum([i for item in rows for i in item if i is not None])

    def fetch_today_cost(self):
        rows = self.db.fetch_by_date()
        store['costs']['dzisiaj'] = sum([i for item in rows for i in item if i is not None])

    #todo: @decorators here to wrapp function and use one method with multiple attributes
    def fetch_week_cost(self):
        rows = self.db.fetch_week()
        if rows:
            store['costs']['w tym tygodniu'] = sum([i for item in rows for i in item])
        else:
            store['costs']['w tym tygodniu'] = 'brak danych'

    def fetch_c_month(self):
        rows = self.db.fetch_current_month()
        store['costs']['w tymm mesiącu'] = sum([i for item in rows for i in item])

    def fetch_l_month(self):
        rows = self.db.fetch_last_mont()
        store['costs']['miesiac wcześniej'] = sum([i for item in rows for i in item])

    def fetch_year(self):
        rows = self.db.all_year()
        store['costs']['w tym roku'] = sum([i for item in rows for i in item])

    def fetch_l_year(self):
        rows = self.db.last_year()
        store['costs']['w poprzednim roku'] = sum([i for item in rows for i in item])






Budget().run()