import sqlite3 as lite
import datetime

class DB:
	def __init__(self, name_db):
		self.connection = lite.connect(name_db)
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

		self.status = TaskStatus()
		self.priority = TaskPriority()

	def execute_query(self, problem, date_today, date_end):
		self.cur.execute('''INSERT INTO TODO(Приоритет, Задача, Статус, Дата_добавления, Дата_окончания) \
		VALUES (?, ?, ?, ?, ?)''', (self.priority.normal, problem, self.status.unperf, date_today, date_end))
		self.connection.commit()

	def update_performed(self, id_, status_):#Функция обновления статуса задачи как "выполнено"
		number = id_
		if status_ == self.status.perf:
			self.cur.execute('''UPDATE TODO SET Статус = ? WHERE № = ?''', (self.status.unperf, number))
		if status_ == self.status.unperf:
			self.cur.execute('''UPDATE TODO SET Статус = ? WHERE № = ?''', (self.status.perf, number))
		self.connection.commit()

	def update_priority(self, id_, priority_):#Функция установление приоритета задачи как "важное"
		number = id_
		if priority_ == self.priority.normal:
			self.cur.execute('''UPDATE TODO SET Приоритет = ? WHERE № = ?''', (self.priority.major, number))
		if priority_ == self.priority.major:
			self.cur.execute('''UPDATE TODO SET Приоритет = ? WHERE № = ?''', (self.priority.normal, number))
		self.connection.commit()


	def update_record(self, new_problem, id_):
		number = id_
		self.cur.execute('''UPDATE TODO SET Задача = ? WHERE № = ?''', (new_problem, number))
		self.connection.commit()


	def clear_all_problems(self):
		self.cur.execute('''DROP TABLE TODO''')
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			Приоритет TEXT, 
  			Задача TEXT NOT NULL,
 			Статус TEXT,		
 			Дата_добавления DATE,
 			Дата_окончания DATE,
 			№ INTEGER PRIMARY KEY AUTOINCREMENT
			)
			""")
		self.connection.commit()

	def delete_problem(self, id_):
		number = id_
		number = tuple([number])
		self.cur.execute('''DELETE FROM TODO WHERE № = ?''', (number))
		self.connection.commit()


	def delete_perfomed_in_bd(self):
		perf = tuple([self.status.perf])
		self.cur.execute('''DELETE FROM TODO WHERE Статус = ?''', (perf))
		self.connection.commit()


	def important_count(self):
		priority_yes = tuple([self.priority.major])
		self.cur.execute('''SELECT * FROM TODO WHERE Приоритет = ?''', (priority_yes)).rowcount
		rows = self.cur.fetchall()
		count_imp = len(rows)
		self.connection.commit()
		return count_imp

	def pass_count(self):
		perf = tuple([self.status.perf])
		self.cur.execute('''SELECT * FROM TODO WHERE Статус = ?''', (perf)).rowcount
		rows = self.cur.fetchall()
		count_perf = len(rows)
		self.connection.commit()
		return count_perf

	def fail_count(self):
		unperf = tuple([self.status.unperf])
		self.cur.execute('''SELECT * FROM TODO WHERE Статус = ?''', (unperf)).rowcount
		rows = self.cur.fetchall()
		count_fail = len(rows)
		self.connection.commit()
		return count_fail

	def all_count(self):
		self.cur.execute('''SELECT * FROM TODO''').rowcount
		rows = self.cur.fetchall()
		count_all = len(rows)
		self.connection.commit()
		return count_all

	def expired_tasks_bd(self):
		str_exp_tasks = 'Просрочено на'
		datetime_today = datetime.date.today()
		self.cur.execute('''SELECT Дата_окончания, № FROM TODO''')
		rows_id = self.cur.fetchall()
		for rows in rows_id:
			date_end_3 = rows[0]
			date_end_3 = date_end_3.split('-')
			date_end_4 = datetime.date(int(date_end_3[0]), int(date_end_3[1]), int(date_end_3[2]))
			if date_end_4 < datetime_today:
				date_exp = datetime_today - date_end_4
				str_exp_tasks = 'Просрочено на ' + str(date_exp.days) + ' д'
				self.cur.execute('''UPDATE TODO SET Статус = ? WHERE № = ?''', (str_exp_tasks, rows[1]))
				self.connection.commit()


class TaskStatus:
	perf = "Выполнено"
	unperf = 'Не выполнено'

class TaskPriority:
	major = 'Важное'
	normal = 'Нет'
