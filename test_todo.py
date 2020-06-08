import unittest
import datetime
import db_todo

class FuncDB:
	def create_db(self):
		self.db = db_todo.DB('test_db.db')
		self.status = db_todo.TaskStatus()
		self.priority = db_todo.TaskPriority()

	def insert_db(self, priority, problem, status, date_end):
		self.date_today = datetime.date.today()
		self.db.cur.execute('''INSERT INTO TODO(Приоритет, Задача, Статус, \
		Дата_добавления, Дата_окончания) \
		VALUES (?, ?, ?, ?, ?)''', (priority, problem, status, self.date_today, date_end))

		self.db.connection.commit()

	def delete_db(self):
		self.db.cur.execute('''DROP TABLE TODO''')
		self.db.connection.commit()

	def fetch_task_by_id(self, id_):
		number = id_
		number = tuple([number])
		self.db.cur.execute('''SELECT * FROM TODO WHERE № = ? ''', (number))
		rows = self.db.cur.fetchall()
		return rows

class TestAddDelete(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()

	def test_add_task_1(self):
		date_today = datetime.date.today()
		date_end_test = datetime.date(2020, 3, 4)
		today_test_str = str(date_today)
		date_end = str(date_end_test)
		problem = 'Трои'
		self.func_db.db.execute_query(problem, date_today, date_end_test)
		id_ = 1
		rows = self.func_db.fetch_task_by_id(id_)
		self.assertEqual(rows, [(self.func_db.priority.normal, problem, \
		self.func_db.status.unperf, today_test_str, date_end, 1)])

	def test_add_task_2(self):
		date_today = datetime.date.today()
		date_end_test = datetime.date(2020, 3, 4)
		today_test_str = str(date_today)
		date_end = str(date_end_test)
		problem = 'Пять'
		self.func_db.db.execute_query(problem, date_today, date_end_test)
		id_ = 2
		rows = self.func_db.fetch_task_by_id(id_)
		self.assertEqual(rows, [(self.func_db.priority.normal, problem, \
		self.func_db.status.unperf, today_test_str, date_end, 2)])

	def test_delete_task_1(self):
		id_ = 1
		self.func_db.db.delete_problem(id_)
		rows = self.func_db.fetch_task_by_id(id_)
		self.assertEqual(rows, [])

	def test_delete_task_2(self):
		id_ = 2
		self.func_db.db.delete_problem(id_)
		rows = self.func_db.fetch_task_by_id(id_)
		self.assertEqual(rows, [])

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()


class TestUpdatePerformed(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()

	def test_update_perf_task_1(self):
		problem_insert = 'Один'
		date_end_insert = datetime.date(2020, 12, 4)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert, \
		self.func_db.status.unperf, date_end_insert)
		id_ = 1
		today_test_str = str(self.func_db.date_today)
		self.func_db.db.update_performed(id_, self.func_db.status.unperf)
		rows = self.func_db.fetch_task_by_id(id_)
		test_date_end = str(datetime.date(2020, 12, 4))
		problem_select = 'Один'
		self.assertEqual(rows, [(self.func_db.priority.normal, problem_select, \
		self.func_db.status.perf, today_test_str, test_date_end, 1)])

	def test_update_perf_task_2(self):
		problem_insert = 'Два'
		date_end_insert = datetime.date(2020, 12, 4)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert, \
		self.func_db.status.perf, date_end_insert)
		id_ = 2
		today_test_str = str(self.func_db.date_today)
		self.func_db.db.update_performed(id_, self.func_db.status.perf)
		rows = self.func_db.fetch_task_by_id(id_)
		test_date_end = str(datetime.date(2020, 12, 4))
		problem_select = 'Два'
		self.assertEqual(rows, [(self.func_db.priority.normal, problem_select, \
		self.func_db.status.unperf, today_test_str, test_date_end, 2)])

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()

class TestUpdatePriority(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()

	def test_update_prior_task_1(self):
		problem_insert = 'Один'
		date_end_insert = datetime.date(2020, 12, 4)
		self.func_db.insert_db(self.func_db.priority.major, problem_insert, \
		self.func_db.status.unperf, date_end_insert)
		id_ = 1
		today_test_str = str(self.func_db.date_today)
		self.func_db.db.update_priority(id_, self.func_db.priority.major)
		rows = self.func_db.fetch_task_by_id(id_)
		test_date_end = str(datetime.date(2020, 12, 4))
		problem_select = 'Один'
		self.assertEqual(rows, [(self.func_db.priority.normal, problem_select, \
		self.func_db.status.unperf, today_test_str, test_date_end, 1)])

	def test_update_prior_task_2(self):
		problem_insert = 'Два'
		date_end_insert = datetime.date(2020, 12, 4)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert, \
		self.func_db.status.unperf, date_end_insert)
		id_ = 2
		today_test_str = str(self.func_db.date_today)
		self.func_db.db.update_priority(id_, self.func_db.priority.normal)
		rows = self.func_db.fetch_task_by_id(id_)
		test_date_end = str(datetime.date(2020, 12, 4))
		problem_select = 'Два'
		self.assertEqual(rows, [(self.func_db.priority.major, problem_select, \
		self.func_db.status.unperf, today_test_str, test_date_end, 2)])

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()

class TestExpTasks(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()

	def test_expired_tasks(self):
		problem_insert = 'Один'
		date_end_insert = datetime.date(2020, 3, 4)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert, \
		self.func_db.status.unperf, date_end_insert)
		self.func_db.db.expired_tasks_bd()
		self.func_db.db.cur.execute('''SELECT Статус, Дата_окончания FROM TODO''')
		rows_id = self.func_db.db.cur.fetchall()
		for id_ in rows_id:
			datetime_today = datetime.date.today()
			date_end_test = datetime.date(2020, 3, 4)
			exp_date = datetime_today - date_end_test
			str_exp_tasks = 'Просрочено на ' + str(exp_date.days) + ' д'
			self.assertEqual(id_[0], (str_exp_tasks))

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()

class TestDeletePerformed(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()

	def test_delete_perf_1(self):
		problem_insert_one = 'Один'
		problem_insert_two = 'Два'
		date_end_insert = datetime.date(2020, 12, 4)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert_one, \
		self.func_db.status.unperf, date_end_insert)
		self.func_db.insert_db(self.func_db.priority.major, problem_insert_two, \
		self.func_db.status.perf, date_end_insert)
		self.func_db.db.delete_perfomed_in_bd()
		id_ = 2
		rows = self.func_db.fetch_task_by_id(id_)
		self.assertEqual(rows, [])

	def test_delete_perf_2(self):
		problem_insert_five = 'Пять'
		date_end_insert = datetime.date(2020, 12, 4)
		test_date_end = str(datetime.date(2020, 12, 4))
		date_today = datetime.date.today()
		today_test_str = str(date_today)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert_five, \
		self.func_db.status.unperf, date_end_insert)
		self.func_db.db.delete_perfomed_in_bd()
		id_ = 3
		rows = self.func_db.fetch_task_by_id(id_)
		self.assertEqual(rows, [(self.func_db.priority.normal, problem_insert_five, \
		self.func_db.status.unperf, today_test_str, test_date_end, 3)])

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()

class TestClearAll(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()

	def test_clear_all(self):
		problem_insert_nine = 'Девять'
		problem_insert_eight = 'Восемь'
		problem_insert_six = 'Шесть'
		date_end_insert = datetime.date(2020, 12, 4)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert_nine, \
		self.func_db.status.unperf, date_end_insert)
		self.func_db.insert_db(self.func_db.priority.major, problem_insert_eight, \
		self.func_db.status.perf, date_end_insert)
		self.func_db.insert_db(self.func_db.priority.major, problem_insert_six, \
		self.func_db.status.unperf, date_end_insert)
		name_db = "test_db.db"
		self.func_db.db.clear_all_problems(name_db)
		self.func_db.db.cur.execute('''SELECT * FROM TODO''')
		rows_id = self.func_db.db.cur.fetchall()
		self.assertEqual(rows_id, [])

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()

class TestInfo(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()
		problem_insert_nine = 'Девять'
		problem_insert_eight = 'Восемь'
		problem_insert_six = 'Шесть'
		date_end_insert = datetime.date(2020, 12, 4)
		cls.func_db.insert_db(cls.func_db.priority.normal, problem_insert_nine, \
		cls.func_db.status.unperf, date_end_insert)
		cls.func_db.insert_db(cls.func_db.priority.major, problem_insert_eight, \
		cls.func_db.status.perf, date_end_insert)
		cls.func_db.insert_db(cls.func_db.priority.major, problem_insert_six, \
		cls.func_db.status.perf, date_end_insert)

	def test_pass_count(self):
		rows = self.func_db.db.pass_count()
		self.assertEqual(rows, 2)

	def test_important_count(self):
		rows = self.func_db.db.important_count()
		self.assertEqual(rows, 2)

	def test_fail_count(self):
		rows = self.func_db.db.fail_count()
		self.assertEqual(rows, 1)

	def test_all_count(self):
		rows = self.func_db.db.all_count()
		self.assertEqual(rows, 3)

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()

class TestChangeProblem(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.func_db = FuncDB()
		cls.func_db.create_db()

	def test_change_problem(self):
		problem_insert_ten = 'Десять'
		date_end_insert = datetime.date(2020, 12, 4)
		self.func_db.insert_db(self.func_db.priority.normal, problem_insert_ten, \
		self.func_db.status.unperf, date_end_insert)
		change_problem_insert = 'Одиннадцать'
		id_ = 1
		today_test_str = str(datetime.date.today())
		self.func_db.db.update_record(change_problem_insert, id_)
		rows = self.func_db.fetch_task_by_id(id_)
		self.assertEqual(rows, [(self.func_db.priority.normal, change_problem_insert,\
		self.func_db.status.unperf, today_test_str, str(date_end_insert), id_)])

	@classmethod
	def tearDownClass(cls):
		cls.func_db.delete_db()

if __name__ == "__main__":
	unittest.main()
