from Mdialog import InfoDialog


def db_insert_dialog(func):
    def wrap(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            if r >= 1:
                InfoDialog(text='Dodano nowy koszt. Przejdż do portfela aby zobaczyć bilans').dialog_()
        except Exception as e:
            print(e)
            #todo: logging with e
            InfoDialog(text='BŁĄD!! koszt nie został dodany. Wykonaj restart i spóbuj ponownie').dialog_()
    return wrap
