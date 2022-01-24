from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from storage import store
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.app import App
from kivy.properties import StringProperty
from Mdialog import InfoDialog
from decor import db_dialog
import re

texts_in = {
    'in_error': 'Niepoprawny format kosztów. Wprowadź koszt zgodnie z wzorcem: np: dziesięć złotych i pięćdziesiat '
                'groszy to: 10.50'
}

cost_input = []


class FirstScreen(MDBottomNavigationItem):
    text_in = StringProperty()

    def _input(self):
        if self.text_in:
            global cost_input
            cost_input.append(self.text_in)


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
                pass    #todo: v.2 - logging module with e, emialclient, internet permission
        else:
            self.data = []
        return self.data


class CatProButton(MDRectangleFlatButton):
    """ add new cost in to db """
    def add_to_db(self):
        global cost_input
        if cost_input:
            cost = cost_input[-1]
            cost = self.validate(cost)
            if cost is not None and cost != 0.0:
                cost, item = str(cost), self.text
                if item in store['category']['cat']:
                    self.ins_cost(cost, None, item)
                elif item in store['project']['pro']:
                    self.ins_cost(cost, item, None)
            else:
                InfoDialog(text=f'{texts_in["in_error"]}').dialog_()
        else:
             InfoDialog(text=f'{texts_in["in_error"]}').dialog_()
        cost_input[:] = []

    def validate(self, cost):
        re_obj = re.compile(r'(^[0-9]+(\.|\,)?((\d)?\d)?$)')  # (^[0-9]+(\.| \,)(?:\d\d?)$)
        match_obj = re_obj.match(cost)
        if match_obj is not None:
            if ',' in cost:
                cost = float(cost.replace(',', '.'))
            return float(cost)

    @db_dialog
    def ins_cost(self, *args):
        app = App.get_running_app().db
        return app.insert_cost(*args)


