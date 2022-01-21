from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from storage import store
from kivymd.uix.button import MDRaisedButton
from kivymd.app import App
from kivy.properties import NumericProperty, StringProperty
from kivy.factory import Factory
from kivymd.uix.textfield import MDTextField

"""  list for costs"""
input_items = []

""" helping methods """
def add_items(par):
    if float(input_items[-1]) > 0:
        cost = input_items[-1]
        item = par
        return cost, item


class FirstScreen(MDBottomNavigationItem):
    """ helping methods with input.text = cost"""
    def add_input_items(self, item):
        input_items.append(item)


class CatView(RecycleView):
    """ RV for Categories """
    def __init__(self, **kwargs):
        super(CatView, self).__init__(**kwargs)
        Clock.schedule_once(self.populate_view)

    def populate_view(self, *args):
        if store['category']['cat']:
            try:
                self.data = [{'text': str(i)} for i in store['category']['cat']]
            except Exception as e:
                print('found exception in CatView')
                #todo: connect this to logger module
        else:
            self.data = []
        return self.data


class ProView(RecycleView):
    """ RV for Projects """
    def __init__(self, **kwargs):
        super(ProView, self).__init__(**kwargs)
        Clock.schedule_once(self.populate_view)

    def populate_view(self, *args):
        if store['project']['pro']:
            try:
                self.data = [{'text': str(i)} for i in store['project']['pro']]
            except Exception as e:
                print('found exception in CatView')
                #todo: connect this to logger module
        else:
            self.data = []
        return self.data


class CatButton(MDRaisedButton):
    """ add new cost in to db """
    def add_to_db(self):
        try:
            cost, cat = add_items(self.text)
        except Exception as e:
            #todo: dialog - no cost to add
            print('no cost to add')
        else:
            app = App.get_running_app().db
            app.insert_cost(cost, None, cat)
        """ recalculate cost in store['costs'] and store['cat_pro'] """
        #todo: App - recalculate fetch_cost


class ProButton(MDRaisedButton):
    """ add new cost in to db """
    def add_to_db(self):
        try:
            cost, pro = add_items(self.text)
        except Exception as e:
            # todo: dialog - no cost to add
            print('no cost to add')
        else:
            app = App.get_running_app().db
            app.insert_cost(cost, pro, None)
        """ recalculate cost in store['costs'] and store['cat_pro'] """
        # todo: App - recalculate fetch_cost + on_leave clear widget in second screen and add new one with new costs !!!! IMPORTANT