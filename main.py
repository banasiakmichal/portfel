""" still in ios branch !!! important """
# set keyboard mode for ios device
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
from kivy.lang.builder import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigation
import SecondScreen
import FirstScreen
import ThirdScreen
from class_mydb import Mydb
from storage import Storage
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.app import MDApp
# from os.path import join
""" set test window and input android keyboard"""
#Window.size = (375, 667)
# Window.softinput_mode = "resize"

kv = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:include FirstScreen.kv
#:include SecondScreen.kv
#:include ThirdScreen.kv

MDScreen:
    Manager:
        id: manager
        #panel_color: get_color_from_hex("#eeeaea")
        #selected_color_background: get_color_from_hex("#97ecf8")
        #text_color_active: 0, 0, 0, 1

        FirstScreen:
            id: screen1
            name: 'screen1'
            text: 'Kasa'
            icon: 'account-cash'
            on_leave:
                screen2.ids.general_view.populate_view()
                screen2.ids.costs_view.populate_view()

        SecondScreen:
            id: screen2
            name: 'screen2'
            text: 'Portfel'
            icon: 'format-list-bulleted-type'

        ThirdScreen:
            name: 'screen3'
            text: 'Ustawienia'
            icon: 'table-settings'
            on_leave:
                screen1.ids.catpro_view.populate_view()
                screen2.ids.general_view.populate_view()
                screen2.ids.costs_view.populate_view()
'''


class Manager(MDBottomNavigation):
    pass


class Budget(MDApp):

    costs_sum = StringProperty('0')
    # store = ''

    # added 27.01
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # init DICTstorage from class Storage() in storage.py for ios device
        self.storage = Storage(self.user_data_dir)
        # self.storage = Storage('') local env
        self.store = self.storage.store
        self.db = Mydb(self.user_data_dir)
        #self.db = Mydb('') local env

    def build(self):
        self.icon = 'logo.png'
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "500"
        return Builder.load_string(kv)

    def on_start(self):
        self.update_store_cat_pro('category', 'project')
        self.update_all()

    def on_pause(self):
        self.db.conn.close()

    def on_stop(self):
        self.db.conn.close()

    """ fetch db methods """
    def update_store_cat_pro(self, *args):
        for i in args:
            rows = self.db.fetch_col(i)
            items = [i for item in rows for i in item if i is not None]
            if i is 'category':
                self.store['category']['cat'] = list(dict.fromkeys(items))
            else:
                self.store['project']['pro'] = list(dict.fromkeys(items))

    def update_procat_costs(self):
        self.db.procat('project', self.store['project']['pro'])
        self.db.procat('category', self.store['category']['cat'])

    def update_gen_cost(self):
        self.fetch_costs()
        self.fetch_general_costs()

    def update_all(self):
        #todo: TEST: fetch from zero db ?
        self.fetch_costs()
        self.fetch_general_costs()
        self.db.procat('project', self.store['project']['pro'])
        self.db.procat('category', self.store['category']['cat'])

    def fetch_costs(self):
        """  all costs for pro, cat and datas source in mydb class"""
        rows = self.db.fetch_col(col='cost')
        self.store['costs']['RAZEM'] = f'{sum([i for item in rows for i in item if i is not None]):.2f}'
        self.costs_sum = f'{(sum([i for item in rows for i in item if i is not None])):.2f}'

    def fetch_general_costs(self):
        """ fetch and pass into localstore all today costs """
        self.fetch_items(self.db.fetch_by_date, 'dzisiaj')
        """ fetch and pass into localstore from curent week """
        self.fetch_items(self.db.fetch_week, 'w tym tygodniu')
        """ fetch and pass into localstore all costs from - current month """
        self.fetch_items(self.db.fetch_current_month, 'w tym miesiącu')
        """ fetch and pass into localstore all costs from - last month """
        self.fetch_items(self.db.fetch_last_mont, 'miesiąc wcześniej')
        """ fetch and pass into localstore all costs from - current year """
        self.fetch_items(self.db.all_year, 'w tym roku')
        """ fetch and pass into local store all cost from last year """
        self.fetch_items(self.db.last_year, 'w poprzednim roku')

    def fetch_items(self, f, ar1):
        """ fetch method"""
        r_ = f()
        self.store['costs'][ar1] = f'{sum([i for item in r_ for i in item]):.2f}'
        return ar1

    def storage(self):
        #app = MDApp.get_running_app()
        #ddir = app.user_data_dir
        self.ddir = self.user_data_dir
        print('with app:', self.ddir)
        print('ddir:', self.user_data_dir + 'STORE')
        # return self.user_data_dir + 'STORE'


Budget().run()