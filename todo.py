from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3 as lite
import datetime
from tkinter import messagebox as mb





###########################################################################################################################################
################################                                  Main                       ##############################################
###########################################################################################################################################

class Main_win: #основное окно
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('ToDo List')
		self.root.geometry("930x600")
		self.root.resizable(False, False)

		x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth())/3.5
		y = (self.root.winfo_screenheight() - self.root.winfo_reqheight())/3.7
		self.root.wm_geometry("+%d+%d" % (x, y))

		self.menubar = Menu(self.root)
		help_ = Menu(self.menubar, tearoff = 0)
		self.menubar.add_cascade(label ='Справка', menu = help_)
		help_.add_command(label ='Помощь', command = self.reference)
		help_.add_command(label ='О приложении', command = self.about)
		self.root.config(menu = self.menubar)


		toolbar = tk.Frame(bg = 'White', width = 930, height = 100)
		toolbar.pack(side = TOP)

		self.tree = ttk.Treeview(self.root, columns = ('important','task','state','date_start','date_end','ID'),
									   height = 100,
									   show = 'headings', selectmode = "browse")

		##
		self.tree.insert('', 'end', text = 'your text', tags = ('oddrow',)) 
		self.tree.tag_configure('oddrow', background='orange')
		###
		self.tree.pack(side = LEFT)

		
		self.tree.column('important', width = 70 , anchor = tk.CENTER)
		self.tree.column('task', width = 510 , anchor = tk.CENTER)
		self.tree.column('state', width = 130 , anchor = tk.CENTER)
		self.tree.column('date_start', width = 110 , anchor = tk.CENTER)
		self.tree.column('date_end', width = 110 , anchor = tk.CENTER)
		self.tree.column('ID', width = 30 , anchor = tk.CENTER)

		
		self.tree.heading('important', text = 'Приоритет')
		self.tree.heading('task', text = 'Задание')
		self.tree.heading('state', text = 'Состояние')
		self.tree.heading('date_start', text = 'Дата Начала')
		self.tree.heading('date_end', text = 'Срок сдачи')
		self.tree.heading('ID',text = 'ID')
		self.tree.bind('<ButtonRelease - 1>', self.select_id_and_date)
		scrollbar = Scrollbar(self.root)
		scrollbar.place(x=915, y=100, height = 500)
		scrollbar.config(command = self.tree.yview)
		self.tree.config(yscrollcommand=scrollbar.set)

		self.make_button(toolbar)

		self.db = db
		self.view_records()
	

	def make_button(self, perent):


		self.add=PhotoImage(file='mainlogos/3.png')
		self.change=PhotoImage(file='mainlogos/6.png')
		self.important=PhotoImage(file='mainlogos/4.png')
		self.delete_pr=PhotoImage(file='mainlogos/2.png')
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
								command = lambda:self.db.update_priority(self.id_),
								bd=3)

		btn_delete = tk.Button(perent,
								text = "delete",
								width = 100,
								height = 100,
								image = self.delete_pr,
								command = lambda:self.delete_problem(),
								bd=3)
		btn_make_performed = tk.Button(perent,
								text = "perfomed",
								width = 100,
								height = 100,
								image = self.performed,
								command = lambda:self.db.update_performed(self.id_),
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
							 	width = 13,
							 	height = 1,
							 	command = lambda:self.info(),
							 	bg = "LightGrey",
							 	bd=2)
		btn_clear_all = tk.Button(perent,
							 	text = "Очистить всё",
							 	width = 13,
							 	height = 1,
							 	command = lambda:self.clear(),
							 	bg = "LightGrey",
							 	bd=2)



		btn_open_add.place 			(x = 5,   y = 0)
		btn_change.place   			(x = 115, y = 0) 
		btn_delete.place			(x = 225, y = 0)	
		btn_important.place 		(x = 335, y = 0)
		btn_make_performed.place 	(x = 445, y = 0)
		btn_delete_performed.place 	(x = 555, y = 0)
		btn_info.place             (x = 664, y = 0)
		btn_clear_all.place			(x = 830, y = 0)


	def run(self):
		self.root.mainloop()

	def records(self,problem,date_today, date_end, problem_str):
		if(problem != ''):
			db.cur.execute('''SELECT Задача,Дата_окончания FROM TODO''')
			rows = db.cur.fetchall()
			i = 0 
			for row in rows:
				if (row[0] == problem) and (row[1] == str(date_end)):
					i = i + 1 
			
			if i == 0:
				self.db.execute_query(problem,date_today, date_end)
			else:
				mb.showinfo("Ошибка", "Вы уже создали такую задачу на этот день")
					
		else:
			mb.showerror("Ошибка", "Поле 'Задача' не должно быть пустым!")
			self.Entry_Error(problem_str)
		self.view_records()
		problem_str.delete(0, 'end')

	def view_records(self):
		self.db.cur.execute('''SELECT * FROM TODO ORDER BY Приоритет''')
		
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values = row) for row in self.db.cur.fetchall()]


	def Entry_Error(self, problem_str):
		problem_str.config(bg = 'pink')

	def select_id_and_date(self, args):
		item = self.tree.selection()[0]
		self.id_  = self.tree.item(item)['values'][-1]
		self.date_end_2 = self.tree.item(item)['values'][4]


	

	def make_add(self):
		Add(self.root)
	def change_problem(self,):
		Change(self.root, self.id_, self.date_end_2)
	def delete_problem(self):
		Delete(self.root)
	def clear(self): # очистить все
		answer = mb.askyesno("Очистить все", "Вы уверены, что хотите удалить все задачи?\nДанная операция полностью удалит все задачи (выполненные и невыполненные) без возможности восстановления")
		if answer == True:
			db.clear_all_problems()
	def delete_performed(self):
		DelPerf(self.root)
	def info(self):
		Info(self.root)
	def about(self):
		About(self.root)
	def reference(self):
		Reference(self.root)



###########################################################################################################################################
################################                                  Add                        ##############################################
###########################################################################################################################################


class Add: #дочернее окно добавления задачи
	def __init__(self, perent):
		self.root2 = tk.Toplevel(perent)
		self.root2.title('Add Task')
		self.root2.geometry("350x130")
		self.root2.resizable(False, False)

		x = (self.root2.winfo_screenwidth() - self.root2.winfo_reqwidth()) / 2.25
		y = (self.root2.winfo_screenheight() - self.root2.winfo_reqheight()) / 1.9
		self.root2.wm_geometry("+%d+%d" % (x, y))

		self.view = main_win
		self.make_window(self.root2)
		




	def make_window(self, root2):
		btn_add_problem = tk.Button(self.root2,
									text = "Add",
									width = 5,
									height = 1,
									command = lambda:self.view.records(self.problem.get(),
																	   self.date_today,
																	   self.Date_end,
																	   self.problem),
									bg = "Green",
									bd=3)

		btn_add_problem.place (x = 100, y = 100)

		self.problem_entry = tk.StringVar()
		self.problem_entry.trace(mode="w", callback=self.validate)

		self.problem = Entry(self.root2, width = 40, textvariable = self.problem_entry)
		self.problem.place(x = 75, y = 5)
		
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
								text = "Close",
								width = 5,
								height = 1,
								command = lambda:self.root2.destroy(),
								bg = "Green",
								bd=3)

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



###########################################################################################################################################
################################                Change                        #############################################################
###########################################################################################################################################

class Change: # дочернее окно изменения задачи
	def __init__(self, perent, id_,date_end ):

		self.db = db

		self.root3 = tk.Toplevel(perent)
		self.root3.title('Изменить')
		self.root3.geometry("500x160")
		self.root3.resizable(False, False)

		x = (self.root3.winfo_screenwidth() - self.root3.winfo_reqwidth()) / 2.5
		y = (self.root3.winfo_screenheight() - self.root3.winfo_reqheight()) / 1.9
		self.root3.wm_geometry("+%d+%d" % (x, y))
		id_for_change = id_

		Label(self.root3, 
			  text = "Введите новый текст в поле ниже:",				
			  font = "Arial 16").place(x=91, y = 40)

		self.new_problem = Entry(self.root3,
								 width = 60)

		btn_change_problem = tk.Button(self.root3,
							 	text = "Изменить",
							 	width = 13,
							 	height = 1,
							 	command = lambda:self.records(self.new_problem.get(), id_for_change,date_end),
							 	bg = "LightGrey",
							 	bd=1)

		self.new_problem.place(x=70, y=70)
		btn_change_problem.place(x = 200, y = 100)

		self.focuse()


	def records(self, problem,id_for_change, date_end):
		if(problem != ''):
			db.cur.execute('''SELECT Задача,Дата_окончания FROM TODO''')
			rows = db.cur.fetchall()
			i = 0 
			for row in rows:
				if (row[0] == problem) and (row[1] == str(date_end)):
					i = i + 1 
			
			if i == 0:
				db.update_record(problem, id_for_change)
				self.root3.destroy()
			else:
				mb.showerror("Ошибка", "Вы уже создали такую задачу на этот день.")
					
		else:
			mb.showerror("Ошибка", "Поле 'Задача' не должно быть пустым!")


	def focuse(self):
		self.root3.grab_set()
		self.root3.focus_set()
		self.root3.wait_window()



###########################################################################################################################################
################################                    Info                      #############################################################
###########################################################################################################################################

class Info: # дочернее окно информации о задачах
	def __init__(self, perent):
		self.db = DB
		self.root7 = tk.Toplevel(perent)
		self.root7.title('Информация')
		self.root7.geometry("250x220")
		self.root7.resizable(False, False)

		x = (self.root7.winfo_screenwidth() - self.root7.winfo_reqwidth()) / 2.1
		y = (self.root7.winfo_screenheight() - self.root7.winfo_reqheight()) / 1.9
		self.root7.wm_geometry("+%d+%d" % (x, y))

		Label(self.root7, text = 'На данный момент:', font = "Arial 15").place(x = 30, y = 10)
		Label(self.root7, text = db.pass_count(), fg = "Green", font = "Arial 13").place(x=20, y=60)
		Label(self.root7, text = db.fail_count(), fg = "Red", font = "Arial 13").place(x=20, y=90)
		Label(self.root7, text = "задач выполнено", fg = "Green", font = "Arial 13").place(x=50, y=60)
		Label(self.root7, text = "задач не выполнено", fg = "Red", font = "Arial 13").place(x=50, y=90)
		Label(self.root7, text = db.important_count(), fg = "Crimson", font = "Arial 13").place(x=20, y=120)
		Label(self.root7, text = "важных задач", fg = "Crimson", font = "Arial 13").place(x=50, y = 120)
		Label(self.root7, text = db.all_count(), font = "Arial 13").place(x=20, y = 150)
		Label(self.root7, text = "задач всего", font = "Arial 13").place(x=50, y =150)

		btn_okay = tk.Button(self.root7,
							 	text = "Окей",
							 	width = 13,
							 	height = 1,
							 	command = lambda:self.root7.destroy(),
							 	bg = "LightGrey",
							 	bd=1)
		btn_okay.place(x = 75, y = 190)			
		self.focuse()

	def focuse(self):
		self.root7.grab_set()
		self.root7.focus_set()
		self.root7.wait_window()

###########################################################################################################################################
################################                            Reference           ###########################################################
###########################################################################################################################################

class Reference: # дочернее окно помощи 
	def __init__(self, perent):
		self.root4 = tk.Toplevel(perent)
		self.root4.title('Справка')
		self.root4.geometry("650x350")
		self.root4.resizable(False, False)

		x = (self.root4.winfo_screenwidth() - self.root4.winfo_reqwidth()) / 2.75
		y = (self.root4.winfo_screenheight() - self.root4.winfo_reqheight()) / 1.9
		self.root4.wm_geometry("+%d+%d" % (x, y))

		self.add=PhotoImage(file='referencelogos/3.png')
		self.change=PhotoImage(file='referencelogos/6.png')
		self.important=PhotoImage(file='referencelogos/4.png')
		self.delete=PhotoImage(file='referencelogos/2.png')
		self.performed=PhotoImage(file='referencelogos/1.png')
		self.delperf=PhotoImage(file='referencelogos/5.png')
		self.information=PhotoImage(file='referencelogos/333.png')
		self.clearall=PhotoImage(file='referencelogos/444.png')
		
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
		Label(self.root4, text = '- нажмите, чтобы увидеть информацию о задачах', font = "Arial 11").place(x=115, y=253)
		img7 = Label(self.root4, image = self.information).place(x = 10, y = 250)
		Label(self.root4, text = '- нажмите, чтобы удалить все задачи (выполненные и невыполненные)', font = "Arial 11").place(x=110, y = 293)
		img8 = Label(self.root4, image = self.clearall).place(x=10, y = 290)

		self.focuse()

	def focuse(self):
		self.root4.grab_set()
		self.root4.focus_set()
		self.root4.wait_window()


###########################################################################################################################################
################################                            About           #############################################################
###########################################################################################################################################

class About: # дочернее окно о приложении
	def __init__(self, perent):
		self.root5 = tk.Toplevel(perent)
		self.root5.title('О приложении')
		self.root5.geometry("930x900")
		self.root5.resizable(False, False)
		self.toolbar1 = PhotoImage(file='referencelogos/421.png')
		self.table1 = PhotoImage(file='referencelogos/422.png')
		
		x = (self.root5.winfo_screenwidth() - self.root5.winfo_reqwidth()) / 3.5
		y = (self.root5.winfo_screenheight() - self.root5.winfo_reqheight()) / 11
		self.root5.wm_geometry("+%d+%d" % (x, y))

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
		Label(self.root5, image = self.toolbar1).place(x=0, y=270)
		Label(self.root5, text = "2. Таблица задач").place(x=20, y = 375)
		Label(self.root5, image = self.table1).place(x=0, y = 395)
		self.focuse()

	def focuse(self):
		self.root5.grab_set()
		self.root5.focus_set()
		self.root5.wait_window()


###########################################################################################################################################
################################                            Delete Perdomed          ######################################################
###########################################################################################################################################
       
class DelPerf: 
	def __init__(self, perent):
		self.root6 = tk.Toplevel(perent)
		self.root6.title('Удалить выполненные')
		self.root6.geometry("330x90")
		self.root6.resizable(False, False)
		txt_dev = Text()

		self.db = db

		x = (self.root6.winfo_screenwidth() - self.root6.winfo_reqwidth()) / 2.25
		y = (self.root6.winfo_screenheight() - self.root6.winfo_reqheight()) / 1.9
		self.root6.wm_geometry("+%d+%d" % (x, y))

		Label(self.root6, text = 'Вы уверены, что хотите удалить выполненные задачи ').place(x=15, rely=.1)
		btn_yes = tk.Button(self.root6,
							 	text = "Да",
							 	width = 3,
							 	height = 1,
							 	command = lambda:self.delete_if_yes(),
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
	def delete_if_yes(self):
		i = 0
		db.cur.execute('''SELECT Статус FROM TODO''')
		rows = db.cur.fetchall()
		for row in rows:
			if row[0] == "Выполнено":
				i+=1
		if i != 0:
			db.delete_perfomed_in_bd()
			self.root6.destroy()
			mb.showinfo("Успешно!", "Все выполненные задачи удалены.")
		else:
			self.root6.destroy()
			mb.showerror("Ошибка!", "Нет ни одной выполененной задачи.")


		
	
	def focuse(self):
		self.root6.grab_set()
		self.root6.focus_set()
		self.root6.wait_window()



###########################################################################################################################################
################################                            DElite                   ######################################################
###########################################################################################################################################


class Delete: # дочернее окно удаления задачи
	def __init__(self, perent):
		self.root8 = tk.Toplevel(perent)
		self.root8.title('Удалить')
		self.root8.geometry("400x100")
		self.root8.resizable(False, False)
		self.main_win = Main_win
		self.db = DB

		x = (self.root8.winfo_screenwidth() - self.root8.winfo_reqwidth()) / 2.25
		y = (self.root8.winfo_screenheight() - self.root8.winfo_reqheight()) / 1.9
		self.root8.wm_geometry("+%d+%d" % (x, y))


		Label(self.root8, text = 'Вы уверены, что хотите удалить эту задачу?' ,
						  font = "Arial 11").place(x=42, rely=.1)
		btn_yes = tk.Button(self.root8,
							 	text = "Да",
							 	width = 3,
							 	height = 1,
							 	command = lambda:self.delete_and_destroy(),
							 	bg = "LightGrey",
							 	bd=1)
		btn_yes.place(relx = .3, rely = .5)
		btn_no = tk.Button(self.root8,
							 	text = "Нет",
							 	width = 3,
							 	height = 1,
							 	command = lambda:self.root8.destroy(),
							 	bg = "LightGrey",
							 	bd=1)
		btn_no.place(relx = .6, rely = .5)
		self.focuse()

	def delete_and_destroy(self):
		db.delete_problem(main_win.id_)
		self.root8.destroy()
		mb.showinfo("Удаление задачи","Задача удалена")

	def focuse(self):
		self.root8.grab_set()
		self.root8.focus_set()
		self.root8.wait_window()

###########################################################################################################################################
################################                            DateBase            ###########################################################
###########################################################################################################################################
        
class DB:
	def __init__(self):
		self.connection = lite.connect("to_do_list.db")
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

	def execute_query(self, problem, date_today, Date_end):

		priority = 'Нет'
	
		status = 'Не выполнено'
		self.cur.execute('''INSERT INTO TODO(Приоритет,Задача, Статус, Дата_добавления, Дата_окончания) VALUES (?,?,?,?, ?)''',
                       (priority,problem, status, date_today, Date_end))
		self.connection.commit()

		

	def update_performed(self, id_):
		status = 'Выполнено'
		number = id_
		self.cur.execute('''UPDATE TODO
      			SET Статус = ?
       			WHERE № = ?
    			''', (status, number))
		self.connection.commit()
		main_win.view_records()

	def update_priority(self, id_):
		priority = 'Важное'
		number = id_
		self.cur.execute('''UPDATE TODO
      			SET Приоритет = ?
       			WHERE № = ?
    			''', (priority, number))
		self.connection.commit()
		main_win.view_records()

	def update_record(self ,new_problem, id_):
		number = id_

		self.cur.execute('''UPDATE TODO
      			SET Задача = ?
       			WHERE № = ?
    			''', (new_problem, number))
		self.connection.commit()
		main_win.view_records()


	def clear_all_problems(self):
		self.cur.execute('''DROP TABLE TODO''')
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
		main_win.view_records()
		mb.showinfo("Готово", "Список задач очищен")

	def delete_problem(self, id_):
		number = id_
		number = tuple([number])
		self.cur.execute('''DELETE FROM TODO WHERE № = ?''', (number))
		self.connection.commit()
		main_win.view_records()

	def delete_perfomed_in_bd(self):
	 	self.cur.execute('''DELETE FROM TODO WHERE Статус = "Выполнено"''')
	 	self.connection.commit()
	 	main_win.view_records()


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

if __name__ == "__main__":

	db = DB()
	main_win = Main_win()
	main_win.run()