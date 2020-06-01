import unittest
import db_todo
import datetime
import sqlite3 as lite

class test_db_add_delete(unittest.TestCase):
	def setUp(self):
		self.db = db_todo.DB("test_db.db")
		self.connection = lite.connect("test_db.db")
		self.cur = self.connection.cursor()
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			Приоритет TEXT, 
  			Задача TEXT NOT NULL,
 			Статус TEXT ,
 			Дата_добавления DATE,
 			Дата_окончания DATE,
 			№ INTEGER PRIMARY KEY AUTOINCREMENT
			)
			""")

		self.connection.commit()

	def test_add_task(self):
		date_end_test = datetime.date(2020,3,4)
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		problem ='Трои'
		self.db.execute_query(problem,date_today_test,date_end_test)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 1 ''')
		rows = self.cur.fetchall()
		self.assertEqual(rows, [('Нет','Трои','Не выполнено',today_test_str,'2020-03-04',1)])

	def test_delete_task(self):
		id_ = 1
		self.db.delete_problem(id_)
		self.cur.execute('''SELECT * FROM TODO WHERE №=1 ''')
		rows_id = self.cur.fetchall()
		self.assertEqual(rows_id, [])

	def tearDown(self):
		self.cur.execute('''DROP TABLE TODO''')
		self.connection.commit()

class test_db_update_perf(unittest.TestCase):
	def setUp(self):
		self.db = db_todo.DB("test_db.db")
		self.connection = lite.connect("test_db.db")
		self.cur = self.connection.cursor()
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			Приоритет TEXT, 
  			Задача TEXT NOT NULL,
 			Статус TEXT ,
 			Дата_добавления DATE,
 			Дата_окончания DATE,
 			№ INTEGER PRIMARY KEY AUTOINCREMENT
			)
			""")

		priority = 'Нет'
		problem = 'Один'
		status = 'Не выполнено'
		date_today = datetime.date.today()
		date_end = datetime.date(2020,12,4)
		self.cur.execute('''INSERT INTO TODO(Приоритет, Задача, Статус, Дата_добавления, Дата_окончания) \
		VALUES (?, ?, ?, ?, ?)''', (priority, problem, status, date_today, date_end))

		self.connection.commit()

	def test_update_perf_task(self):
		status_ = 'Не выполнено'
		id_ = 1
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		self.db.update_performed(id_, status_)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 1 ''')
		rows = self.cur.fetchall()
		status_test = 'Выполнено'
		test_date_end = str(datetime.date(2020,12,4))
		problem = 'Один'
		priority = 'Нет'
		self.assertEqual(rows, [(priority,problem,status_test,today_test_str,test_date_end,1)])

	def tearDown(self):
		self.cur.execute('''DROP TABLE TODO''')
		self.connection.commit()

class test_db_exp_tasks(unittest.TestCase):
	def setUp(self):
		self.db = db_todo.DB("test_db.db")
		self.connection = lite.connect("test_db.db")
		self.cur = self.connection.cursor()
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			Приоритет TEXT, 
  			Задача TEXT NOT NULL,
 			Статус TEXT ,
 			Дата_добавления DATE,
 			Дата_окончания DATE,
 			№ INTEGER PRIMARY KEY AUTOINCREMENT
			)
			""")

		priority = 'Нет'
		problem = 'Один'
		status = 'Не выполнено'
		date_today = datetime.date.today()
		date_end = datetime.date(2020,3,4)
		self.cur.execute('''INSERT INTO TODO(Приоритет, Задача, Статус, Дата_добавления, Дата_окончания) \
		VALUES (?, ?, ?, ?, ?)''', (priority, problem, status, date_today, date_end))

		self.connection.commit()

	def test_expired_tasks(self):
		self.db.expired_tasks_bd()
		self.cur.execute('''SELECT Статус, Дата_окончания FROM TODO''')
		rows_id = self.cur.fetchall()
		for id_ in rows_id:
			datetime_today = datetime.date.today()
			date_end_test = datetime.date(2020,3,4)
			exp_date = datetime_today - date_end_test
			str_exp_tasks = 'Просрочено на ' + str(exp_date.days) + ' д'
			self.assertEqual(id_[0], (str_exp_tasks))

	def tearDown(self):
		self.cur.execute('''DROP TABLE TODO''')
		self.connection.commit()

class test_db_del_perf(unittest.TestCase):
	def setUp(self):
		self.db = db_todo.DB("test_db.db")
		self.connection = lite.connect("test_db.db")
		self.cur = self.connection.cursor()
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			Приоритет TEXT, 
  			Задача TEXT NOT NULL,
 			Статус TEXT ,
 			Дата_добавления DATE,
 			Дата_окончания DATE,
 			№ INTEGER PRIMARY KEY AUTOINCREMENT
			)
			""")

		priority = 'Нет'
		problem = 'Один'
		status = 'Не выполнено'
		date_today = datetime.date.today()
		date_end = datetime.date(2020,12,4)
		self.cur.execute('''INSERT INTO TODO(Приоритет, Задача, Статус, Дата_добавления, Дата_окончания) \
		VALUES (?, ?, ?, ?, ?)''', (priority, problem, status, date_today, date_end))

		self.connection.commit()

	def test_delete_perf(self):
		self.db.delete_perfomed_in_bd()
		self.cur.execute('''SELECT * FROM TODO WHERE №=2 ''')
		rows_id = self.cur.fetchall()
		self.assertEqual(rows_id, [])

	def tearDown(self):
		self.cur.execute('''DROP TABLE TODO''')
		self.connection.commit()

class test_db_clr_all(unittest.TestCase):
	def setUp(self):
		self.db = db_todo.DB("test_db.db")
		self.connection = lite.connect("test_db.db")
		self.cur = self.connection.cursor()
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			Приоритет TEXT, 
  			Задача TEXT NOT NULL,
 			Статус TEXT ,
 			Дата_добавления DATE,
 			Дата_окончания DATE,
 			№ INTEGER PRIMARY KEY AUTOINCREMENT
			)
			""")

		priority = 'Нет'
		problem = 'Один'
		status = 'Не выполнено'
		date_today = datetime.date.today()
		date_end = datetime.date(2020,12,4)
		self.cur.execute('''INSERT INTO TODO(Приоритет, Задача, Статус, Дата_добавления, Дата_окончания) \
		VALUES (?, ?, ?, ?, ?)''', (priority, problem, status, date_today, date_end))

		self.connection.commit()

	def test_clear_all(self):
		self.db.clear_all_problems()
		self.cur.execute('''SELECT * FROM TODO''')
		rows_id = self.cur.fetchall()
		self.assertEqual(rows_id, [])

if __name__ == "__main__":
	unittest.main()
	