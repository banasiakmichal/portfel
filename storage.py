from kivy.storage.dictstore import DictStore

#todo: use Pathlib modul do find path for os and android
store = DictStore('STORE')

""" initialize storages """
store['category'] = {'cat': []}
store['project'] = {'pro': []}

""" general costs"""
store['costs'] = {}

