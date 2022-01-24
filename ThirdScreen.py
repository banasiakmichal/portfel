from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from storage import store
from Mdialog import InfoDialog
from kivymd.app import App
from decor import db_dialog

texts = {
    'in_1': 'Wybrana nazwa nie może być użyta. Istnieje już taka pozycja. Podaj inną nazwę',
    'in_2': 'Wskazana nazwa nie spełnia kryteriów. Jest pustym polem lub jest za długa. Maks. ilość znaków to 15'
}


class ThirdScreen(MDBottomNavigationItem):
    dialog =None

    """ add category and project into local storage and db  -  main methods """

    def add_cat(self, cat):
        self.add_to_db(cat, store['category']['cat'])

    def add_pro(self, pro):
        self.add_to_db(pro, store['project']['pro'])

    def del_cat(self, catpro, item):
        self.del_item(catpro, item, store['category']['cat'])

    def del_pro(self, catpro, item):
        self.del_item(catpro, item, store['project']['pro'])

    def add_to_db(self, catpro, storage):
        """ add to local storage, insert into db with validation """
        item = catpro.upper()
        if item != '' and len(item) < 15:
            if item not in store['category']['cat'] and item not in store['project']['pro']:
                storage.append(catpro.upper())
                app = App.get_running_app().db
                if storage is store['category']['cat']:
                    self.db_item(app.insert_cost('0', None, catpro.upper()))
                elif storage is store['project']['pro']:
                    self.db_item(app.insert_cost('0', catpro.upper(), None))
            else:
                 InfoDialog(text=f'{texts["in_1"]}').dialog_()
        else:
            InfoDialog(text=f'{texts["in_2"]}').dialog_()

    def del_item(self, catpro, item, storage):
        """ del category or project from storage and db"""
        item = item.upper()
        if item in storage:
            storage.remove(item)
            store['catpro'].pop(item)
            app = App.get_running_app().db
            self.db_item(app.del_item(catpro, item))
        else:
            InfoDialog(text=f'w {self.helper(catpro)} nie ma pozycji {item}, sprobuj usunać z drugiego zbioru, jeśli komunikat wyświetli'
                            f' sie ponownie, sprawdź pisownie i upewnij się że taka pozycja istnieje w Twoim portfelu').dialog_()

    def helper(self, catpro):
        if catpro == 'category':
            return 'kategoriach'
        else:
            return 'projektach'

    @db_dialog
    def db_item(self, f):
        return f

    @ db_dialog
    def clear_db_(self):
        store['category']['cat'] = []
        store['project']['pro'][:] = []
        store['costs'].clear()
        store['catpro'].clear()
        app = App.get_running_app().db
        return app.clear_db()



