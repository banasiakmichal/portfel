from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from storage import store
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.app import App
from kivy.properties import StringProperty
from kivy.factory import Factory
import re

cost_in = None

class FirstScreen(MDBottomNavigationItem):
    text_in = StringProperty()

    def validate_input(self):
        if self.text_in:
            re_obj = re.compile(r'(^[0-9]+(\.|\,)(?:\d\d?)$)')
            match_obj = re_obj.match(self.text_in)
            print('match_obj', match_obj)
            if match_obj is not None:
                if ',' in self.text_in:
                    global cost_in
                    cost_in = float(self.text_in.replace(',', '.'))
                else:
                    cost_in = self.text_in
                    print('global cost:', cost_in)
        else:
            pass
            # todo: dialog here:wprowadz prawidłową wartosć kosztów


class CatProView(RecycleView):
    """ RV for Categories """
    def __init__(self, **kwargs):
        super(CatProView, self).__init__(**kwargs)
        Clock.schedule_once(self.populate_view)

    def populate_view(self, *args):
        if store['category']['cat'] or store['project']['pro']:
            # join lists
            new_store = [*store['category']['cat'], *store['project']['pro']]
            try:
                self.data = [{'text': str(i)} for i in new_store]
            except Exception as e:
                print('found exception in CatView')
                #todo: connect this to logger module
        else:
            self.data = []
        return self.data


class CatProButton(MDRectangleFlatButton):
    """ add new cost in to db """
    def add_to_db(self):
        global cost_in
        if cost_in is not None and cost_in != 0.0:
            cost = str(cost_in)
            print('cost', cost)
            item = self.text
            app = App.get_running_app().db
            #todo: correct this
            if item in store['category']['cat'] and item in store['project']['pro']:
                app.insert_cost(cost, None, item)
                app.insert_cost(cost, item, None)
            else:
                if item in store['category']['cat'] and item not in store['project']['pro']:
                # for cat
                    app.insert_cost(cost, None, item)
                elif item in store['project']['pro'] and item not in store['category']['cat']:
                # for project
                    app.insert_cost(cost, item, None)

            cost_in = None

            #todo: dialog: koszt został pomyślnie dodany -- lepiej -- slider!!!




        """ recalculate cost in store['costs'] and store['cat_pro'] """
        #todo: App - recalculate fetch_cost
