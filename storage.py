from kivy.storage.dictstore import DictStore
from os.path import join

#todo: use Pathlib modul do find path for os and android


class Storage():

    def __init__(self, path):
        self.path = path
        self.store = DictStore(join(self.path, 'STORE'))
        #/Users/michalbanasiak/Library/Application Support/budget/STORE
        """ initialize storages """
        self.store['category'] = {'cat': []}
        self.store['project'] = {'pro': []}
        """ general costs"""
        self.store['costs'] = {}
        """ costs for category and projects"""
        self.store['catpro'] = {}
