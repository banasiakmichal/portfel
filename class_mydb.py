import sqlite3, datetime
from decimal import Decimal
from kivymd.app import MDApp
from os.path import join


class Mydb:
    # create date attr
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    year = int(today[:4])
    month = int(Decimal(today[5:7]))
    # attr for weekly costs [self.calendar methods]
    day_start = ''
    day_end = ''

    """ crete table with: date, project, category, cost"""
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(join(self.path, "budget.db"))
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS budget "
                         "(date TEXT, project TEXT, category TEXT, cost INT)")
        self.calendar()

    """ insert new cost into table"""
    def insert_cost(self, cost, project, category):
        self.cur.execute("insert into budget values (?, ?, ?, ?)", (self.today, project, category, cost,))
        self.conn.commit()
        return self.conn.total_changes

    """ fetch data and cost from category or projects """
    def fetch_cost_and_data(self, catpro, item):
        q = state = f"SELECT cost, date from budget WHERE {catpro} = '{item}'"
        rows = self.cur.execute(q).fetchall()
        return rows

    """ fetch costs from table"""
    def fetch_col(self, col='project'): return self.cur.execute(f"SELECT {col} from budget").fetchall()

    """ fetch cost by date where """
    def fetch_by_date(self): return self.cur.execute(f"SELECT cost from budget WHERE date = '{self.today}'").fetchall()

    def fetch_week(self): return self.cur.execute(f"Select cost from budget WHERE date BETWEEN '{self.day_start}' and '{self.day_end}'").fetchall()

    def fetch_current_month(self): return self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.year)}-{self.today[5:7]}%'").fetchall()

    def fetch_last_mont(self): return self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.year)}-{self.get_month()}%'").fetchall()

    """ fetch all records with year """
    def all_year(self): return self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.year)}%'").fetchall()

    def last_year(self): return self.cur.execute(f"Select cost from budget WHERE date LIKE '%{str(self.year-1)}%'").fetchall()

    def cat_pro_costs(self, catpro, stor, *args):
        """ summary costs for items in category and projects """
        if stor:
            store = MDApp.get_running_app().store
            for it in stor:
                    rows = self.cur.execute(f"SELECT cost from budget WHERE {catpro} = '{it}'").fetchall()
                    store['costs'][it] = sum([i for item in rows for i in item])

    def calendar(self):
        """ calendar function for weekly cost calculate """
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
            store = MDApp.get_running_app().store
            for item in stor:
                state = f"SELECT cost from budget WHERE {param} = '{item}'"
                # get all costs for all items in category and project
                rows = self.cur.execute(state).fetchall()
                store['catpro'][item] = [sum([i for item in rows for i in item])]
                # get all for item from last week
                rows_w = self.cur.execute(f"{state} AND date BETWEEN '{self.day_start}' and '{self.day_end}'").fetchall()
                store['catpro'][item].append(sum([i for item in rows_w for i in item]))
                # get all for item from current month
                #todo: correct this in product app
                rows_m = self.cur.execute(f"{state} AND date LIKE '%{str(self.year)}-{self.today[5:7]}%'").fetchall()
                store['catpro'][item].append(sum([i for item in rows_m for i in item]))

    def get_month(self):
        """ helping func to get month number """
        #todo: correct this method in prod app
        m = self.month - 1
        if m == 0:
            return str(12)
        elif m in range(1, 10):
            return '0' + str(m)
        elif m in range(10, 12):
            return str(m)

    def del_item(self, catpro, item):
        query = f"DELETE from budget WHERE {catpro} = ?"
        self.cur.execute(query, (item,))
        self.conn.commit()
        return self.cur.rowcount

    def clear_db(self):
        self.cur.execute("DELETE from budget;")
        self.conn.commit()
        return self.cur.rowcount

