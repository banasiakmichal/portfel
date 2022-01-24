from Mdialog import InfoDialog


def db_dialog(func):
    def wrap(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            if r >= 1:
                InfoDialog(text='MAMY TO!, działanie zakończyło się powodzeniem.').dialog_()
        except Exception as e:
            print(e)   #todo: logging with e v2.0
            InfoDialog(text='UPSS - BŁĄD!! wyłącz aplikacje i spróbuj ponownie').dialog_()
    return wrap
