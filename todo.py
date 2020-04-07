import tkinter as tk

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
		self.root2.geometry("300x200")
		self.root2.resizable(False, False)

		self.focuse()

	def focuse(self):
		self.root2.grab_set()
		self.root2.focus_set()
		self.root2.wait_window()
		

if __name__ == "__main__":
	main_win = Main_win()
	#main_win.make_add()
	main_win.run()
	

