from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from storage import store

#todo: clear oll cost from db ---> new layout - new budget !!!


class ThirdScreen(MDBottomNavigationItem):

    """ add and del category and projects into store (store.py)"""
    def add_cat(self, cat):
        if cat not in store['category']['cat'] and cat != '':
            store['category']['cat'].append(cat)
        else:
            pass #:todo dialog with massage

    def del_cat(self, cat):
        try:
            store['category']['cat'].remove(cat)
        except Exception as e:
            pass
            # todo: dialog here with information - there is no such category
        finally:
            #todo: change this order
            pass

    def add_pro(self, pro):
        if pro not in store['project']['pro'] and pro != '':
            store['project']['pro'].append(pro)
        else:
            pass  #todo: dialog - there is project like this

    def del_pro(self, pro):
        try:
            store['project']['pro'].remove(pro)
        except Exception as e:
            pass
            # todo: dialog here with information - there is no such category
        finally:
            pass