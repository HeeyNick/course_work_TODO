import unittest
import db_todo
import datetime
import sqlite3 as lite

class test_db(unittest.TestCase):
	def setUp(self):
		self.db = db_todo.DB("test_db.db")

	def create_db(self):
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

	def test_aadd_task(self):
		self.create_db()
		date_end_test = datetime.date(2020,12,4)
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		problem ='Трои'
		self.db.execute_query(problem,date_today_test,date_end_test)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 1 ''')
		rows = self.cur.fetchall()
		self.assertEqual(rows, [('Нет','Трои','Не выполнено',today_test_str,'2020-12-04',1)])

	def test_aadd_task_1(self):
		self.create_db()
		date_end_test = datetime.date(2020,12,4)
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		problem ='Семь'
		self.db.execute_query(problem,date_today_test,date_end_test)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 2 ''')
		rows = self.cur.fetchall()
		self.assertEqual(rows, [('Нет','Семь','Не выполнено',today_test_str,'2020-12-04',2)])

	def test_aadd_task_2(self):
		self.create_db()
		date_end_test = datetime.date(2020,12,4)
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		problem ='Восемь'
		self.db.execute_query(problem,date_today_test,date_end_test)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 3 ''')
		rows = self.cur.fetchall()
		self.assertEqual(rows, [('Нет','Восемь','Не выполнено',today_test_str,'2020-12-04',3)])

	def test_bcount_fail(self):
		self.create_db()
		rows = self.db.fail_count()
		self.assertEqual(rows, 3)

	def test_bcount_all(self):
		self.create_db()
		rows = self.db.all_count()
		self.assertEqual(rows, 3)

	def test_cupdate_perf_task(self):
		self.create_db()
		status_ = 'Не выполнено'
		id_ = 2
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		self.db.update_performed(id_, status_)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 2 ''')
		rows = self.cur.fetchall()
		self.assertEqual(rows, [('Нет','Семь','Выполнено',today_test_str,'2020-12-04',2)])

	def test_dcount_pass(self):
		self.create_db()
		rows = self.db.pass_count()
		self.assertEqual(rows, 1)

	def test_eupdate_priora(self):
		self.create_db()
		prior_ = 'Нет'
		id_ = 1
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		self.db.update_priority(id_, prior_)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 1 ''')
		rows = self.cur.fetchall()
		self.assertEqual(rows, [('Важное','Трои','Не выполнено',today_test_str,'2020-12-04',1)])

	def test_fcount_important(self):
		self.create_db()
		rows = self.db.important_count()
		self.assertEqual(rows, 1)

	def test_gupdate_priora_2(self):
		self.create_db()
		prior_ = 'Важное'
		id_ = 1
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)		
		self.db.update_priority(id_, prior_)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 1 ''')
		rows = self.cur.fetchall()
		
		self.assertEqual(rows, [('Нет','Трои','Не выполнено',today_test_str,'2020-12-04',1)])

	def test_hupdate_record(self):
		self.create_db()
		id_ = 1
		new_problem = 'Четыре'
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		self.db.update_record(new_problem, id_)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 1 ''')
		rows = self.cur.fetchall()
		
		self.assertEqual(rows, [('Нет','Четыре','Не выполнено',today_test_str,'2020-12-04',1)])

	def test_iupdate_record_2(self):
		self.create_db()
		id_ = 1
		new_problem = 'Трои'
		date_today_test = datetime.date.today()
		today_test_str = str(date_today_test)
		self.db.update_record(new_problem, id_)
		self.cur.execute('''SELECT * FROM TODO WHERE №= 1 ''')
		rows = self.cur.fetchall()
		self.assertEqual(rows, [('Нет','Трои','Не выполнено',today_test_str,'2020-12-04',1)])

	def test_jdelete_perf(self):
		self.create_db()
		self.db.delete_perfomed_in_bd()
		self.cur.execute('''SELECT * FROM TODO WHERE №=2 ''')
		rows_id = self.cur.fetchall()
		self.assertEqual(rows_id, [])

	def test_kdelete_task(self):
		self.create_db()
		id_ = 3
		self.db.delete_problem(id_)
		self.cur.execute('''SELECT * FROM TODO WHERE №=3 ''')
		rows_id = self.cur.fetchall()
		self.assertEqual(rows_id, [])

	def test_lclear_all(self):
		self.create_db()
		self.db.clear_all_problems()
		self.cur.execute('''SELECT * FROM TODO''')
		rows_id = self.cur.fetchall()
		self.assertEqual(rows_id, [])

	def test_mexpired_tasks(self):
		self.create_db()
		self.db.expired_tasks_bd()
		self.cur.execute('''SELECT Статус FROM TODO''')
		rows_id = self.cur.fetchall()
		for id_ in rows_id:
			if id_[0] != 'Выполнено':
				datetime_today = datetime.date.today()
				date_end_test = datetime.date(2020,3,4)
				exp_date = datetime_today - date_end_test
				str_exp_tasks = 'Просрочено на ' + str(exp_date.days) + ' д'
				self.assertEqual(id_[0], (str_exp_tasks))

if __name__ == "__main__":
	unittest.main()
