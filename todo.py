from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3 as lite
import datetime
from tkinter.tix import *
from tkinter import messagebox as mb

###################################################################
####################Графическая оболочка###########################
###################################################################

class Main_win: #основное окно
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('ToDo List')
		self.root.geometry("900x600")
		self.root.resizable(False, False)

		self.menubar = Menu(self.root)
		help_ = Menu(self.menubar, tearoff = 0)
		self.menubar.add_cascade(label ='Справка', menu = help_)
		help_.add_command(label ='Помощь', command = self.reference)
		help_.add_command(label ='О приложении', command = self.about)
		self.root.config(menu = self.menubar)

		toolbar = tk.Frame(bg = 'White', width = 900, height = 100)
		toolbar.place ( x =0, y = 0)

		self.tree = ttk.Treeview(self.root, columns = ('ID','important','task','state','date_start','date_end'),
									   height = 100,
									   show = 'headings')

		self.tree.heading('ID', text = 'ID')
		self.tree.heading('important', text = 'Приоритет')
		self.tree.heading('task', text = 'Задание')
		self.tree.heading('state', text = 'Состояние')
		self.tree.heading('date_start', text = 'Дата Начала')
		self.tree.heading('date_end', text = 'Срок сдачи')

		self.tree.column('ID', width = 30 , anchor = tk.CENTER)
		self.tree.column('important', width = 60 , anchor = tk.CENTER)
		self.tree.column('task', width = 490 , anchor = tk.CENTER)
		self.tree.column('state', width = 130 , anchor = tk.CENTER)
		self.tree.column('date_start', width = 100 , anchor = tk.CENTER)
		self.tree.column('date_end', width = 100 , anchor = tk.CENTER)

		self.tree.place(x=0,y=100)

		self.make_button(toolbar)

		self.db = db
		self.view_records()

	def make_button(self, perent):

		self.add=PhotoImage(file='mainlogos/3.png')
		self.change=PhotoImage(file='mainlogos/6.png')
		self.important=PhotoImage(file='mainlogos/4.png')
		self.delete=PhotoImage(file='mainlogos/2.png')
		self.performed=PhotoImage(file='mainlogos/1.png')
		self.delperf=PhotoImage(file='mainlogos/5.png')
		

		btn_open_add = tk.Button(perent,
								text = "Add Task",
								width = 100,
								height = 100,
								image= self.add,
								bd=3,
								command = lambda:self.make_add())
		
		btn_change = tk.Button(perent,
								text = "Change",
								width = 100,
								height = 100,
								image= self.change,
								command = lambda:self.change_problem(),
								
								bd=3)

		btn_important = tk.Button(perent,
								text = "important",
								width = 100,
								height = 100,
								image = self.important,
								#command = lambda:self.make_add(),
								bd=3)

		btn_delete = tk.Button(perent,
								text = "delete",
								width = 100,
								height = 100,
								image = self.delete,
								#command = lambda:self.make_add(),
								bd=3)
		btn_make_performed = tk.Button(perent,
								text = "perfomed",
								width = 100,
								height = 100,
								image = self.performed,
								#command = lambda:self.make_add(),
								bd=3)

		btn_delete_performed = tk.Button(perent,
								text = "del perfomed",
								width = 100,
								height = 100,
								image = self.delperf,
								command = lambda:self.delete_performed(),
								bd=3)
		btn_info = tk.Button(perent,
							 	text = "Информация",
							 	width = 15,
							 	height = 1,
							 	command = lambda:self.info(),
							 	bg = "LightGrey",
							 	bd=3)


		btn_open_add.place 			(x = 5,   y = 0)
		btn_change.place   			(x = 115, y = 0) 
		btn_delete.place			(x = 225, y = 0)	
		btn_important.place 		(x = 335, y = 0)
		btn_make_performed.place 	(x = 445, y = 0)
		btn_delete_performed.place 	(x = 555, y = 0)
		btn_info.place             (x = 735, y = 0)

	def run(self):
		self.root.mainloop()

	def records(self,problem,date_today, date_end, problem_str):
		if(problem != ''):
			self.db.execute_query(problem,date_today, date_end)
		else:
			mb.showerror("Ошибка", "Поле 'Задача' не должно быть пустым!")
			self.Entry_Error(problem_str)

		self.view_records()
		problem_str.delete(0, 'end')

	def view_records(self):
		self.db.cur.execute('''SELECT * FROM TODO''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values = row) for row in self.db.cur.fetchall()]

	def Entry_Error(self, problem_str):
		problem_str.config(bg = "Pink")


	'''def print_problem_add_task(self, result_number, result_status, result_problem, result_date_now, result_date_end):
		number = int(result_number[0][0])
		Label(self.root, text=result_number, font = "Times 16").place(x = 50 , y = 150  + (number - 1) * 50  )
		status_problem = result_problem + '    ' + result_status + '   ' + result_date_now + '   ' + result_date_end #
		Label(self.root, text=status_problem, font = "Times 16").place(x = 90 , y = 150 + (number - 1) * 50)'''


########Тест чтобы вызвать дочернее окно , потом назначить на кнопку##

	def reference(self):
		Reference(self.root)

	def about(self):
		About(self.root)

	def make_add(self):
		Add(self.root)

	def info(self):
		Info(self.root)

	def delete_performed(self):
		DelPerf(self.root)

	def make_performed(self):
		Perf(self.root)

	def change_problem(self):
		Change(self.root)

class Add: #дочернее окно
	def __init__(self, perent):
		self.root2 = tk.Toplevel(perent)
		self.root2.title('Добавить')
		self.root2.geometry("350x130")
		self.root2.resizable(False, False)

		self.view = main_win
		self.make_window(self.root2)

	def make_window(self, root2):

		self.problem_entry = tk.StringVar()
		self.problem_entry.trace(mode="w", callback=self.validate)

		self.problem = Entry(self.root2, width = 40, textvariable = self.problem_entry)
		self.problem.place(x = 75, y = 5)

		btn_add_problem = tk.Button(self.root2,
									text = "Добавить",
									width = 10,
									height = 1,
									command = lambda:self.view.records(self.problem.get(),
													self.date_today,
													self.Date_end,
													self.problem),
									bg = "LightGrey",
									bd=1)

		btn_add_problem.place (x = 85, y = 100)
		
		Label(self.root2, text = 'Задача').place(x = 10, y = 5)

		Label(self.root2, text = 'Дата окончания').place(x = 10, y = 35)

		self.date_today = datetime.date.today()

		self.Day = tk.IntVar()
		self.Month = tk.IntVar()
		self.Year = tk.IntVar()

		self.Day.set(self.date_today.day)
		self.Month.set(self.date_today.month)
		self.Year.set(self.date_today.year)

		self.Day_spin = Spinbox(self.root2,
								width=3,
								from_ = 1, to = 31, 
								textvariable=self.Day, 
								command = self.date_less_today)

		self.Day_spin.place(x = 45, y = 65)

		Label(self.root2, text = 'День').place(x = 10, y = 65)

		self.Month_spin = Spinbox(self.root2, 
								  width = 3, 
								  from_=1, 
								  to=12, 
								  textvariable=self.Month, 
								  command = self.date_less_today)

		self.Month_spin.place(x = 135, y = 65)

		Label(self.root2, text = 'Месяц').place(x = 85, y = 65)

		self.Year_spin = Spinbox(self.root2,
								 width = 5,
								 from_= 2020, 
								 to=9999, 
								 textvariable=self.Year, 
								 command = self.date_less_today)
		self.Year_spin.place(x = 195, y = 65)
		Label(self.root2, text = 'Год').place(x = 170, y = 65)


		self.Date_end = datetime.date(self.Year.get(), self.Month.get(), self.Day.get())



		btn_add_destroy = tk.Button(self.root2,
								text = "Закрыть",
								width = 10,
								height = 1,
								command = lambda:self.root2.destroy(),
								bg = "LightGrey",
								bd=1)

		btn_add_destroy.place (x = 190, y = 100)

		self.input_Date_end()

		self.focuse()


	def focuse(self):
		self.root2.grab_set()
		self.root2.focus_set()
		self.root2.wait_window()

	def date_less_today(self):
		self.Year_t = int(self.Year.get())
		self.Month_t = int(self.Month.get())
		self.Day_t = int(self.Day.get())

		self.change_spin()

	def change_spin(self):
		if(self.Year_t < self.date_today.year or self.Year_t == self.date_today.year):
			if(self.Month_t <  self.date_today.month or self.Month_t == self.date_today.month):
				if(self.Day_t < self.date_today.day):
					self.Day_spin.config(from_ = self.date_today.day)
				self.Month_spin.config(from_= self.date_today.month)
			self.Year_spin.config(from_ = self.date_today.year)

		if(self.Year_t == self.date_today.year and self.Month_t > self.date_today.month):
			self.Day_spin.config(from_ = 1)

		if(self.Year_t > self.date_today.year):
			self.Month_spin.config(from_= 1)
			self.Day_spin.config(from_ = 1)

		self.input_Date_end()

	def input_Date_end(self):
		self.Date_end = datetime.date(self.Year.get(), self.Month.get(), self.Day.get())

	def validate(self, *args):
		self.problem.config(bg = 'white')

class Change: 
	def __init__(self, perent):
		self.root3 = tk.Toplevel(perent)
		self.root3.title('Изменить')
		self.root3.geometry("500x160")
		self.root3.resizable(False, False)

		s = 1
		name = tk.StringVar()
		name.set(12)

		self.cp_label = Label(self.root3, text = "Вы выбрали задачу под ID:", font= "Arial 12").place(x=140,y=10)
		self.id_label = Label(self.root3, text = s, font = "Arial 12").place(x=340, y=10)
		Label(self.root3, text = "Введите новый текст в поле ниже:", font = "Arial 11").place(x=135, y = 55)
		self.cp = Entry(self.root3, textvariable=name, width = 60).place(x=70, y=80)
		btn_change_problem = tk.Button(self.root3,
							 	text = "Изменить",
							 	width = 13,
							 	height = 1,
							 	command = lambda:self.root3.destroy(),
							 	bg = "LightGrey",
							 	bd=1)
		btn_change_problem.place(x = 200, y = 110)

		self.focuse()

	def focuse(self):
		self.root3.grab_set()
		self.root3.focus_set()
		self.root3.wait_window()

class Info: 
	def __init__(self, perent):
		self.root7 = tk.Toplevel(perent)
		self.root7.title('Информация')
		self.root7.geometry("300x200")
		self.root7.resizable(False, False)

		pass_count = tk.StringVar()
		pass_count.set(12)
		fail_count = tk.StringVar()
		fail_count.set(14)
		Label(self.root7, text = 'На данный момент:', font = "Arial 15").place(x = 60, y = 10)
		Label(self.root7, textvariable = pass_count, fg = "Green", font = "Arial 13").place(x=20, y=60)
		Label(self.root7, textvariable = fail_count, fg = "Red", font = "Arial 13").place(x=20, y=90)
		Label(self.root7, text = "задач выполнено", fg = "Green", font = "Arial 13").place(x=50, y=60)
		Label(self.root7, text = "задач не выполнено", fg = "Red", font = "Arial 13").place(x=50, y=90)

		btn_okay = tk.Button(self.root7,
							 	text = "Окей",
							 	width = 13,
							 	height = 1,
							 	command = lambda:self.root7.destroy(),
							 	bg = "LightGrey",
							 	bd=1)
		btn_okay.place(x = 100, y = 140)			
		self.focuse()

	def focuse(self):
		self.root7.grab_set()
		self.root7.focus_set()
		self.root7.wait_window()

class Reference: 
	def __init__(self, perent):
		self.root4 = tk.Toplevel(perent)
		self.root4.title('Справка')
		self.root4.geometry("550x300")
		self.root4.resizable(False, False)
		self.add=PhotoImage(file='referencelogos/3.png')
		self.change=PhotoImage(file='referencelogos/6.png')
		self.important=PhotoImage(file='referencelogos/4.png')
		self.delete=PhotoImage(file='referencelogos/2.png')
		self.performed=PhotoImage(file='referencelogos/1.png')
		self.delperf=PhotoImage(file='referencelogos/5.png')
		self.information=PhotoImage(file='referencelogos/333.png')
		Label(self.root4, text = '- нажмите, чтобы добавить задачу', font = "Arial 11").place(x=40, y=13)
		img1 = Label(self.root4, image = self.add).place(x = 10, y = 10)
		Label(self.root4, text = '- выделив задачу, нажмите, чтобы изменить текст задачи', font = "Arial 11").place(x=40, y=53)
		img2 = Label(self.root4, image = self.change).place(x = 10, y = 50)
		Label(self.root4, text = '- выделив задачу, нажмите, чтобы пометить задачу как важную', font = "Arial 11").place(x=40, y=93)
		img3 = Label(self.root4, image = self.important).place(x = 10, y = 90)
		Label(self.root4, text = '- выделив задачу, нажмите, чтобы удалить задачу', font = "Arial 11").place(x=40, y=133)
		img4 = Label(self.root4, image = self.delete).place(x = 10, y = 130)
		Label(self.root4, text = '- выделив задачу, нажмите, чтобы отметить задачу как выполненную', font = "Arial 11").place(x=40, y=173)
		img5 = Label(self.root4, image = self.performed).place(x = 10, y = 170)
		Label(self.root4, text = '- нажмите, чтобы удалить все задачи, отмеченные как выполненные', font = "Arial 11").place(x=40, y=213)
		img6 = Label(self.root4, image = self.delperf).place(x = 10, y = 210)
		Label(self.root4, text = '- нажмите, чтобы увидеть информацию о задачах', font = "Arial 11").place(x=130, y=253)
		img7 = Label(self.root4, image = self.information).place(x = 10, y = 250)
		self.focuse()

	def focuse(self):
		self.root4.grab_set()
		self.root4.focus_set()
		self.root4.wait_window()

class About: 
	def __init__(self, perent):
		self.root5 = tk.Toplevel(perent)
		self.root5.title('О приложении')
		self.root5.geometry("900x900")
		self.root5.resizable(False, False)
		Label(self.root5, text = "TODO LIST", font = "Arial 15").place(x=375, y=20)
		Label(self.root5, text = "Приложение TODO LIST содержит следующие функции:", font = "Arial 11").place(x = 20, y = 60)
		Label(self.root5, text = "1. Добавление задачи в список дел;").place(x=20, y = 90)
		Label(self.root5, text = "2. Изменение текста задачи в списке дел;").place(x=20, y = 110)
		Label(self.root5, text = "3. Удаление задачи из списка дел;").place(x=20, y = 130)
		Label(self.root5, text = "4. Помечание задачи как важной;").place(x=20, y = 150)
		Label(self.root5, text = "5. Отмечание задачи как выполненной;").place(x=20, y = 170)
		Label(self.root5, text = "6. Удаление всех задач, отмеченных, как выполненные.").place(x=20, y = 190)
		Label(self.root5, text = "Основное окно приложения содержит:", font = "Arial 11").place(x=20, y =220)
		Label(self.root5, text = "1. Меню. (подробнее о меню - Справка -> Помощь)").place(x=20, y = 250)
		self.focuse()

	def focuse(self):
		self.root5.grab_set()
		self.root5.focus_set()
		self.root5.wait_window()
       
class DelPerf: 
	def __init__(self, perent):
		self.root6 = tk.Toplevel(perent)
		self.root6.title('Удалить выполненные')
		self.root6.geometry("330x90")
		self.root6.resizable(False, False)
		txt_dev = Text()
		Label(self.root6, text = 'Вы уверены, что хотите удалить выполненные задачи?').place(x=15, rely=.1)
		btn_yes = tk.Button(self.root6,
							 	text = "Да",
							 	width = 3,
							 	height = 1,
							 	command = lambda:self.root6.destroy(),
							 	bg = "LightGrey",
							 	bd=1)
		btn_yes.place(relx = .3, rely = .5)
		btn_no = tk.Button(self.root6,
							 	text = "Нет",
							 	width = 3,
							 	height = 1,
							 	command = lambda:self.root6.destroy(),
							 	bg = "LightGrey",
							 	bd=1)
		btn_no.place(relx = .6, rely = .5)
		self.focuse()

	def focuse(self):
		self.root6.grab_set()
		self.root6.focus_set()
		self.root6.wait_window()
        
class DB:
	def __init__(self):
		self.connection = lite.connect("to_do_list.db")
		self.cur = self.connection.cursor()
		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS TODO (
  			№ INTEGER PRIMARY KEY AUTOINCREMENT,
  			Приоритет TEXT, 
  			Задача TEXT NOT NULL,
 			Статус TEXT ,
 			Дата_добавления DATE,
 			Дата_окончания DATE
			)
			""")

		self.connection.commit()

	def execute_query(self, problem, date_today, Date_end):

		priority = 'Нет'
	
		status = 'Не выполнено'
		self.cur.execute('''INSERT INTO TODO(Приоритет,Задача, Статус, Дата_добавления, Дата_окончания) VALUES (?,?,?,?, ?)''',
                       (priority,problem, status, date_today, Date_end))
		self.connection.commit()

		'''self.cur.execute("SELECT № FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_number = self.cur.fetchall()
		self.cur.execute("SELECT Задача FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_problem = self.cur.fetchall()
		self.cur.execute("SELECT Статус FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_status = self.cur.fetchall()
		self.cur.execute("SELECT Дата_окончания FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_date_end = self.cur.fetchall()
		self.cur.execute("SELECT Дата_добавления FROM TODO ORDER BY № DESC LIMIT 1;")
		self.result_date_now = self.cur.fetchall()
		self.result_status = str(self.result_status[0][0])
		self.result_problem = str(self.result_problem[0][0])
		self.result_date_end = str(self.result_date_end[0][0])
		self.result_date_now = str(self.result_date_now[0][0])
		self.date_end_numeral = [int(x) for x in self.result_date_end.split("-")]
		day_end = int(self.date_end_numeral[2])
		month_end =int(self.date_end_numeral[1])
		year_end = int(self.date_end_numeral[0])
		self.date_end_less = datetime.date(year_end, month_end, day_end)

		print(self.date_end_numeral)
		problem_str.delete(0,'end')
		main_win.print_problem_add_task(self.result_number, self.result_status, self.result_problem, self.result_date_now, self.result_date_end)'''



if __name__ == "__main__":

	db = DB()
	main_win = Main_win()
	main_win.run()
	

