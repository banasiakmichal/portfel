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
        return self.conn.total_changes

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
        rows = self.cur.execute(f"Select cost from budget WHERE date LIKE '%{self.year}-{self.get_month()}%'").fetchall()
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
            for it in stor:
                    rows = self.cur.execute(f"SELECT cost from budget WHERE {catpro} = '{it}'").fetchall()
                    store['costs'][it] = sum([i for item in rows for i in item])

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

    def procat(self, param, stor):
        ''' all cost in category item and project item
         list[0] = all costs, list[1] - last week costs, list[2] - last month  '''

        if stor:
            for item in stor:
                state = f"SELECT cost from budget WHERE {param} = '{item}'"
                # get all costs for all items in category and project
                rows = self.cur.execute(state).fetchall()
                store['catpro'][item] = [sum([i for item in rows for i in item])]
                # get all for item from last week
                rows_w = self.cur.execute(f"{state} AND date BETWEEN '{self.day_start}' and '{self.day_end}'").fetchall()
                store['catpro'][item].append(sum([i for item in rows_w for i in item]))
                # get all for item from last month
                rows_m = self.cur.execute(f"{state} AND date LIKE '%{str(self.month)}%'").fetchall()
                store['catpro'][item].append(sum([i for item in rows_m for i in item]))

    def get_month(self):
        """ helping func to get month number """
        m = str(self.month - 1)
        if m == '0':
            m = str(12)
        return m

    def del_item(self, catpro, item):
        query = f"DELETE from budget WHERE {catpro} = ?"
        self.cur.execute(query, (item,))
        self.conn.commit()
        return self.cur.rowcount

    def clear_db(self):
        self.cur.execute("DELETE from budget;")
        self.conn.commit()
        print(self.cur.rowcount)
        return self.cur.rowcount


    #def insertdb(self):
        #with closing(self.conn) as connection:
            #with closing(self.cur) as cursor:
