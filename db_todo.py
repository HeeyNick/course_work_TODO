import sqlite3 as lite


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

	def execute_query(self, problem, date_today, date_end):
		priority = 'Нет'
		status = 'Не выполнено'
		self.cur.execute('''INSERT INTO TODO(Приоритет, Задача, Статус, Дата_добавления, Дата_окончания) \
		VALUES (?, ?, ?, ?, ?)''', (priority, problem, status, date_today, date_end))
		self.connection.commit()

	def update_performed(self, id_, status_):#Функция обновления статуса задачи как "выполнено"
		number = id_
		if status_ == 'Выполнено':
			status = 'Не выполнено'
			self.cur.execute('''UPDATE TODO SET Статус = ? WHERE № = ?''', (status, number))
		if status_ == 'Не выполнено':
			status = 'Выполнено'
			self.cur.execute('''UPDATE TODO SET Статус = ? WHERE № = ?''', (status, number))
		self.connection.commit()

	def update_priority(self, id_, priority_):#Функция установление приоритета задачи как "важное"
		number = id_
		if priority_ == 'Нет':
			priority = 'Важное'
			self.cur.execute('''UPDATE TODO SET Приоритет = ? WHERE № = ?''', (priority, number))
		if priority_ == 'Важное':
			priority = 'Нет'
			self.cur.execute('''UPDATE TODO SET Приоритет = ? WHERE № = ?''', (priority, number))
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
	 	self.cur.execute('''DELETE FROM TODO WHERE Статус = "Выполнено"''')
	 	self.connection.commit()


	def important_count(self):
		self.cur.execute('''SELECT * FROM TODO WHERE Приоритет = "Важное"''').rowcount
		rows = self.cur.fetchall()
		count_imp = len(rows)
		self.connection.commit()
		return count_imp

	def pass_count(self):
		self.cur.execute('''SELECT * FROM TODO WHERE Статус = "Выполнено"''').rowcount
		rows = self.cur.fetchall()
		count_perf = len(rows)
		self.connection.commit()
		return count_perf

	def fail_count(self):
		self.cur.execute('''SELECT * FROM TODO WHERE Статус = "Не выполнено"''').rowcount
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