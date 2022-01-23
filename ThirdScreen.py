from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from storage import store
from Mdialog import MyDialog, InfoDialog
from kivymd.app import App

texts = {
    'db-ok': 'pozycja została pomyślnie dodana to Twojej Listy w sekcji: Ogólne. Możesz dodać koszty',
    'db_del_ok' : 'pozycja została usunięta',
    'error': 'Niestety coś poszło nie tak. Uruchom ponownie aplikacje, jeśli błąd bedzie występował'
                                'prosimy o kontakt z dostawcą. Email kontaktowy: portfel.admin#gmail.com',
    'in_1': 'Wybrana nazwa nie może być użyta. Istnieje już taka pozycja. Podaj inną nazwę',
    'in_2': 'Wskazana nazwa nie spełnia kryteriów. Jest pustym polem lub jest za długa. Maks. ilość znaków to 15'
}


class ThirdScreen(MDBottomNavigationItem):
    dialog =None

    def dialogs_wrapper(func):
        """ decorator with dialogs for input field"""
        def wrap(*args, **kwargs):
            if func(*args, **kwargs) >= 1: #todo: tutaj jest error gdy usunę baze danych
                #todo: crate new backaup db - and backup every week - if no main db connect to backup. evry week del and back up !!!
                InfoDialog(text=f'{args[1]}, {texts["db-ok"]}').dialog_()
            else:
                InfoDialog(text=f'{texts["error"]}').dialog_() # todo: + loogging plus wysłanie mailem usterki
        return wrap

    def db_wrapper(func):
        """ decorator with dialogs for db insert items"""
        def wrap(*args, **kwargs):
            item = args[1].upper()
            if item != '' and len(item) < 15:
                #todo: lower and uperrcase validation: !!!!important
                if item not in store['category']['cat'] and item not in store['project']['pro']:
                    func(*args, *kwargs)
                else:
                    InfoDialog(text=f'{texts["in_1"]}').dialog_()
            else:
                InfoDialog(text=f'{texts["in_2"]}').dialog_()
        return wrap

    """ add category and project into local storage and db  -  main methods """
    #todo: what can I do with one line functions
    def add_cat(self, cat):
        self.add_to_db(cat, store['category']['cat'])

    def add_pro(self, pro):
        self.add_to_db(pro, store['project']['pro'])

    def del_cat(self, catpro, item):  # store['category']['cat']
        self.del_item(catpro, item, store['category']['cat'])

    def del_pro(self, catpro, item):
        self.del_item(catpro, item, store['project']['pro'])

    """  thers included methods"""

    @db_wrapper
    def add_to_db(self, catpro, storage):
        """ add to local storage, insert into db with validation """
        storage.append(catpro.upper())
        self.add_proof(catpro.upper(), storage)

    @dialogs_wrapper
    def add_proof(self, catpro, storage):
        """ show dialog id insert is True nad error dialog if insert is False"""
        app = App.get_running_app().db
        if storage is store['category']['cat']:
            try:
                r_ = app.insert_cost('0', None, catpro.upper())
            except Exception as e:
                print(ConnectionError)  #todo: logging module  + email_client, v.2.1
            else:
                return r_
        elif storage is store['project']['pro']:
            try:
                r_ = app.insert_cost('0', catpro.upper(), None)
            except Exception as e:
                print(ConnectionError)  #todo: logging module  + email_client v.2.1
            return r_


    def del_item(self, catpro, item, storage):
        """ del category or project from storage and db"""
        item = item.upper()
        print('item', item)
        print(store['category']['cat'])
        if item in storage:
            storage.remove(item)
            app = App.get_running_app().db
            try:
                r = app.del_item(catpro, item)

            except Exception as e:
                print(e)
                InfoDialog(text=f'{texts["error"]}').dialog_()  #todo: logging module  + email_client v.2.1

            else:
                if r >= 1:
                    InfoDialog(text=f'{texts["db_del_ok"]}').dialog_()
        else:
            InfoDialog(text=f'w {catpro} nie ma pozycji {item}, sprobuj usunać z drugiego zbioru, jeśli komunikat wyświetli'
                            f' sie ponownie, sprawdź pisownie i upewnij się że taka pozycja istnieje w Twoim portfelu').dialog_()

    def clear_db_(self):
        app = App.get_running_app().db
        store['category']['cat'] = []
        store['project']['pro'][:] = []
        store['costs'].clear()
        store['catpro'].clear()
        print(store['costs'], store['catpro'])

        try:
            r = app.clear_db()
        except Exception as e:
            InfoDialog(text=f'{texts["error"]}').dialog_()
            #todo: logging with e
        else:
            if r >= 1:
                InfoDialog(text='Portfel został wyczyszczony. Możesz teraz wprowadzić nowe koszty.').dialog_()
            else:
                InfoDialog(text=f'{texts["error"]}').dialog_()



