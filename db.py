import sqlite3


#sql ='''CREATE TABLE EMPLOYEE(
#   FIRST_NAME CHAR(20) NOT NULL,
#   LAST_NAME CHAR(20),
#   AGE INT,
#   SEX CHAR(1),
#   INCOME FLOAT
#)'''


class db():
    def __init__(self, path):
        self.__conn = sqlite3.connect(path)
        self.__cur = self.__conn.cursor()

        ## Create users table
        #self.__cur.execute('''CREATE TABLE users
        #             (user_id INTEGER PRIMARY KEY,
        #              user_name TEXT)''')

        ## Create tasks table
        #self.__cur.execute('''CREATE TABLE tasks
        #             (id INTEGER PRIMARY KEY,
        #              task_name TEXT,
        #              to_be_done_date TEXT,
        #              is_done INTEGER,
        #              user_id TEXT)''')
        #self.__conn.commit()
        pass

    def is_consist(self, user_id):        
        self.__cur.execute(f"SELECT * FROM users WHERE user_id='{user_id}';")
        results = self.__cur.fetchall()
        if len(results) == 0:
            return False
        return True
        

    def add_task(self, name, p_date, id):
        self.__cur.execute(f"""INSERT INTO tasks(task_name, to_be_done_date, is_done, user_id) 
                            VALUES('{name}', '{p_date}', '{0}', '{id}');""")
        self.__conn.commit()
        pass

    def add_user(self, id, name):
        self.__cur.execute(f"""INSERT INTO users(user_id, user_name) 
                            VALUES('{id}', '{name}');""")
        self.__conn.commit()
        pass

    def get_dates(self, id):
        self.__cur.execute(f"SELECT to_be_done_date FROM tasks WHERE user_id='{id}'")
        results = self.__cur.fetchall()
        return results

    def set_done(self, tname):
        self.__cur.execute(f'''
                                UPDATE tasks SET is_done = True WHERE task_name = '{tname}';        
                            ''')
        self.__conn.commit()
        pass

    def get_users_id(self):
        self.__cur.execute(f"SELECT user_id FROM users;")
        results = self.__cur.fetchall()        
        return results

    def get_state_by_date(self, date):
        self.__cur.execute(f"SELECT is_done FROM tasks WHERE to_be_done_date='{date}'")
        res = self.__cur.fetchall()
        return res

    def get_task_by_date(self, date):
        self.__cur.execute(f"SELECT task_name FROM tasks WHERE to_be_done_date='{date}';")
        res = self.__cur.fetchall()
        return res

    def show_tasks(self, id):
        self.__cur.execute(f"SELECT * FROM tasks WHERE user_id='{id}';")
        results = self.__cur.fetchall()
        return results

    def delete_task(self):
        self.__cur.execute(f"DELETE FROM tasks WHERE is_done=1;")
        self.__conn.commit()
    pass