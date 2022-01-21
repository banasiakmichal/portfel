import sqlite3, datetime
from decimal import Decimal
from storage import store
from contextlib import closing


class Mydb:
    # create date attr
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    year = int(today[:4])
    month = int(Decimal(today[5:7]))
    # attr for weekly costs [self.calendar methods]
    day_start = ''
    day_end = ''

    # create dbconn attr
    #todo: create appropriate path for db --> ios,mac, android
    conn = sqlite3.connect("budget.db")
    cur = conn.cursor()

    """ crete table with: date, project, category, cost"""
    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS budget "
                         "(date TEXT, project TEXT, category TEXT, cost INT)")
        self.calendar()

    """ insert new cost into table"""
    def insert_cost(self, cost, project, category):
        self.cur.execute("insert into budget values (?, ?, ?, ?)", (self.today, project, category, cost,))
        self.conn.commit()
        print(self.conn.total_changes)
        pass

    """ fetch costs from table"""
    def fetch_col(self, col='project'):
        rows = self.cur.execute(f"SELECT {col} from budget").fetchall()
        return rows

    """ fetch cost by date where """
    def fetch_by_date(self):
        rows = self.cur.execute(f"SELECT cost from budget WHERE date = '{self.today}'").fetchall()
        return rows

    def fetch_week(self):
        rows = self.cur.execute(f"Select cost from budget WHERE date BETWEEN '{self.day_start}' and '{self.day_end}'").fetchall()
        return rows

    def fetch_current_month(self):
        rows = self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.month)}%'").fetchall()
        return rows

    def fetch_last_mont(self):
        m = str(self.month-1)
        if m == '0':
            m = str(12)
        rows = self.cur.execute(f"Select cost from budget WHERE date LIKE '%{self.year}-{m}%'").fetchall()
        return rows

    #def all_year(self):
        #""" fetch all records with year"""
        #rows = self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.year)}%'").fetchall()
        #return rows

    """ fetch all records with year """
    #todo: correct all one line functions
    def all_year(self): return self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.year)}%'").fetchall()

    def last_year(self):
        rows = self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.year-1)}%'").fetchall()
        return rows

    def cat_pro_costs(self, catpro, stor, *args):
        """ summary costs for items in category and projects """
        if stor:
            print(stor)
            for it in stor:
                    rows = self.cur.execute(f"SELECT cost from budget WHERE {catpro} = '{it}'").fetchall()
                    store['costs'][it] = sum([i for item in rows for i in item])
                    print(store['costs'][it])

    def calendar(self):
        """ calendar function for weekly cost calculate """
        #todo: test this script with unittest for allyear!!! IMPORTANT
        days = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
        n_d = datetime.datetime.now().strftime('%a')  # Sun
        d = int(Decimal(self.today[-2:]))
        for key, value in days.items():
            if key == n_d:
                self.day_end = f'{self.today[:4]}-{self.today[5:7]}-{7 - value + d}'
                self.day_start = f'{self.today[:4]}-{self.today[5:7]}-{d - value + 1}'


"""

    #def insertdb(self):
        #with closing(self.conn) as connection:
            #with closing(self.cur) as cursor:

"""
