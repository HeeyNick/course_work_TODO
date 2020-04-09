import tkinter as tk
from tkinter import *
import sqlite3 as lite
import datetime

class DB:
	def __init__(self):
		self.connection = lite.connect("to_do_list.db")
		self.cur = self.connection.cursor()
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			№ INTEGER PRIMARY KEY AUTOINCREMENT,
  			Задача TEXT NOT NULL,
 			Статус TEXT ,
 			Дата_добавления DATE,
 			Дата_окончания DATE
			)
			""")

		self.connection.commit()

	def execute_query(self, problem, date_today, Day, Month, Year, problem_str):
	
		Date_end = datetime.date(Year, Month, Day)
		
		status = 'Not_perfomed'
		self.cur.execute('''INSERT INTO TODO(Задача, Статус, Дата_добавления, Дата_окончания) VALUES (?,?,?, ?)''',
                       (problem, status, date_today, Date_end))
		self.connection.commit()

		self.cur.execute("SELECT № FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_number = self.cur.fetchall()
		self.cur.execute("SELECT Задача FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_problem = self.cur.fetchall()
		self.cur.execute("SELECT Статус FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_status = self.cur.fetchall()
		self.cur.execute("SELECT Дата_окончания FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_date_end = self.cur.fetchall()
		self.cur.execute("SELECT Дата_добавления FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_date_now = self.cur.fetchall()
		problem_str.delete(0,'end')
		main_win.print_problem(self.result_number, self.result_status, self.result_problem, self.result_date_now, self.result_date_end)

####################Графическая оболочка###########################


class Main_win: #основное окно
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('ToDo List')
		self.root.geometry("900x600")
		self.root.resizable(False, False)

		toolbar = tk.Frame(bg = 'Grey', width = 900, height = 100)
		toolbar.place ( x =0, y = 0)

		self.make_button(toolbar)

	def print_problem(self, result_number, result_status, result_problem, result_date_now, result_date_end):
		Label(self.root, text=result_number, font = "Times 16").place(x = 50 , y = 150  )
		Label(self.root, text=result_problem, font = "Times 16").place(x = 90 , y = 150 )

		print(result_status)
		print(result_date_now)
		print(type(result_number))
		print(result_number)
		number = int(result_number[0][0])
		print(number)
		print(type(number))
		Label(self.root, text=result_status, font = "Times 16").place(x = 150 , y = 150 )
		Label(self.root, text=result_date_now, font = "Times 16").place(x = 340 , y = 150 )
		Label(self.root, text=result_date_end, font = "Times 16").place(x = 450 , y = 150 )

	def make_button(self, perent):
		btn_open_add = tk.Button(perent,
								text = "Add Task",
								width = 14,
								height = 10,
								command = lambda:self.make_add(),
								bg = "Green",
								bd=3)
		
		btn_change = tk.Button(perent,
								text = "Change",
								width = 14,
								height = 10,
								command = lambda:self.make_add(),
								bg = "Green",
								bd=3)

		btn_important = tk.Button(perent,
								text = "important",
								width = 14,
								height = 10,
								command = lambda:self.make_add(),
								bg = "Green",
								bd=3)

		btn_delete = tk.Button(perent,
								text = "delete",
								width = 14,
								height = 10,
								command = lambda:self.make_add(),
								bg = "Green",
								bd=3)
		btn_make_performed = tk.Button(perent,
								text = "perfomed",
								width = 14,
								height = 10,
								command = lambda:self.make_add(),
								bg = "Green",
								bd=3)

		btn_delete_performed = tk.Button(perent,
								text = "del perfomed",
								width = 14,
								height = 10,
								command = lambda:self.make_add(),
								bg = "Green",
								bd=3)




		btn_open_add.place 			(x = 0,   y = 0)
		btn_change.place   			(x = 115, y = 0) 
		btn_delete.place			(x = 230, y = 0)	
		btn_important.place 		(x = 345, y = 0)
		btn_make_performed.place 	(x = 460, y = 0)
		btn_delete_performed.place 	(x = 575, y = 0)


	def run(self):
		self.root.mainloop()


########Тест чтобы вызвать дочернее окно , потом назначить на кнопку##

	def make_add(self):
		Add(self.root)

class Add: #дочернее окно
	def __init__(self, perent):
		self.root2 = tk.Toplevel(perent)
		self.root2.title('Add Task')
		self.root2.geometry("350x130")
		self.root2.resizable(False, False)

		btn_add_problem = tk.Button(self.root2,
								text = "Add",
								width = 5,
								height = 1,
								command = lambda:db.execute_query(self.problem.get(),self.date_today,self.Day.get(),self.Month.get(),self.Year.get(),self.problem),
								bg = "Green",
								bd=3)

		btn_add_problem.place (x = 100, y = 100)


		self.problem = Entry(self.root2, width = 40)
		self.problem.place(x = 75, y = 5)
		
		Label(self.root2, text = 'Задача').place(x = 10, y = 5)

		Label(self.root2, text = 'Дата окончания').place(x = 10, y = 35)

		self.date_today = datetime.date.today()

		self.Day = tk.IntVar()
		self.Month = tk.IntVar()
		self.Year = tk.IntVar()

		self.Day_spin = Spinbox(self.root2, width=3, from_ = 1, to = 31, textvariable=self.Day)
		self.Day_spin.place(x = 45, y = 65)
		Label(self.root2, text = 'День').place(x = 10, y = 65)

		self.Month_spin = Spinbox(self.root2, width = 3, from_=1, to=12, textvariable=self.Month)
		self.Month_spin.place(x = 135, y = 65)
		Label(self.root2, text = 'Месяц').place(x = 85, y = 65)

		self.Year_spin = Spinbox(self.root2, width = 5,from_= 2020, to=9999, textvariable=self.Year)
		self.Year_spin.place(x = 195, y = 65)
		Label(self.root2, text = 'Год').place(x = 170, y = 65)

		btn_add_problem = tk.Button(self.root2,
								text = "Close",
								width = 5,
								height = 1,
								command = lambda:self.root2.destroy(),
								bg = "Green",
								bd=3)

		btn_add_problem.place (x = 190, y = 100)


		self.focuse()

	def focuse(self):
		self.root2.grab_set()
		self.root2.focus_set()
		self.root2.wait_window()


if __name__ == "__main__":
	db = DB()
	main_win = Main_win()
	#main_win.make_add()
	main_win.run()
	

