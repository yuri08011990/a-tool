from tkinter import *
from tkinter.tix import *
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import sys




class MainWindow:


	date_of_sale = 'Date of sale'
	volume = 'Volume'
	margin = 1.36
	output_price = 'Output price'
	input_price = 'Input price'
	roi = 'ROI'




	def __init__ (self, master):
		frame = Frame(master)
		frame.pack()
		self.createWidgets()


	def createWidgets(self):
		menu = Menu(root)
		root.config(menu=menu)


		fileMenu = Menu(menu, tearoff=0)
		menu.add_cascade(label="File", menu=fileMenu)
		fileMenu.add_command(label="Open", command=self.open_file)
		fileMenu.add_command(label="Save as", command=self.save_file)
		fileMenu.add_separator()
		fileMenu.add_command(label="Quit", command=root.destroy)

		toolsMenu = Menu(menu, tearoff=0)
		menu.add_cascade(label="Tools", menu=toolsMenu)
		toolsMenu.add_command(label="Run calculations", command=self.calculations)
		toolsMenu.add_command(label="Plot graph", command=self.graph)

		helpMenu = Menu(menu, tearoff=0)
		menu.add_cascade(label="Help", menu=helpMenu)
		helpMenu.add_command(label="Help", command=self.help_window)
		helpMenu.add_separator()
		helpMenu.add_command(label="About", command=self.about_window)


		toolbar = Frame(root, bd=1, relief=SUNKEN)

		openButton = Button(toolbar, image=openButton_icon, command=self.open_file)
		openButton.pack(side=LEFT, padx=2, pady=2)
		ToolTip1 = Balloon()
		ToolTip1.bind_widget(openButton, balloonmsg="Open a .csv file")
		saveButton = Button(toolbar, image=saveButton_icon, command=self.save_file)
		saveButton.pack(side=LEFT, padx=2, pady=2)
		ToolTip2 = Balloon()
		ToolTip2.bind_widget(saveButton, balloonmsg="Save as")
		calculateButton = Button(toolbar, image=calculationsButton_icon, command=self.calculations)
		calculateButton.pack(side=LEFT, padx=2, pady=2)
		ToolTip3 = Balloon()
		ToolTip3.bind_widget(calculateButton, balloonmsg="Perform calculations")
		graphButton = Button(toolbar, image=graphButton_icon, command=self.graph)
		graphButton.pack(side=LEFT, padx=2, pady=2)
		ToolTip4 = Balloon()
		ToolTip4.bind_widget(graphButton, balloonmsg="Plot graph")
		quitButton = Button(toolbar, image=quitButton_icon, command=root.quit)
		quitButton.pack(side=RIGHT, padx=2, pady=2)
		ToolTip5 = Balloon()
		ToolTip5.bind_widget(quitButton, balloonmsg="Exit the program")
		helpButton = Button(toolbar, image=helpButton_icon, command=self.help_window)
		helpButton.pack(side=RIGHT, padx=2, pady=2)
		ToolTip6 = Balloon()
		ToolTip6.bind_widget(helpButton, balloonmsg="View help information")

		toolbar.pack(side=TOP, fill=X)

		global statusbar
		statusbar = Label(root, text='Welcome to A-Tool', bd=1, relief=SUNKEN, anchor=W)
		statusbar.pack(side=BOTTOM, fill=X)


	def open_file(self):
		try:
			input_file = filedialog.askopenfilename(filetypes = (("CSV Files","*.csv"),))
			self.df = pd.read_csv(input_file)
			statusbar['text'] = 'File ' + input_file + ' loaded successfully!'
		except:
			statusbar['text'] = 'No files were loaded'


	def save_file(self):
		try:
			output_file = filedialog.asksaveasfilename(filetypes = (("CSV Files","*.csv"),))
			self.df.to_csv(output_file, index=False, encoding='utf8')		
			l1 = Label(root, text='Result saved to file')
			l1.pack()
			statusbar['text'] = 'Result saved to ' + output_file
		except:
			statusbar['text'] = 'Saving to file cancelled'


	def help_window(self):
		root = Tk()
		root.title("A-Tool - Інструкції")
		root.geometry("530x100")
		root.columnconfigure(0, weight=1)
		root.resizable(FALSE,FALSE)
		P = Text(root)
		P.pack(expand=True, fill=BOTH)
		P.insert(END, "1. Load .csv file\n")
		P.insert(END, "2. Press 'Run calculations'\n")
		P.insert(END, "3. Press 'Plot graph'\n")
		P.insert(END, "3. Press 'Save file in .csv'")


	def about_window(self):
		root = Tk()
		root.title("A-Tool; - Про програму")
		root.geometry("550x70")
		root.columnconfigure(0, weight=1)
		root.resizable(FALSE,FALSE)
		P = Text(root)
		P.pack(expand=True, fill=BOTH)
		P.insert(END, "A-Tool is a multipurpose analysis tool\n")
		P.insert(END, "Created by Yuri Skavinski")
	
	
	def calculations(self):
		try:
			self.df[self.date_of_sale] = pd.to_datetime(self.df[self.date_of_sale])
			self.df[self.output_price] = (self.df[self.input_price]) * self.margin
			self.df[self.roi] = ((self.df[self.volume]) * (self.df[self.output_price])) - ((self.df[self.volume] * self.df[self.input_price]))
			self.df = self.df[[self.date_of_sale, self.volume, self.input_price, self.output_price, self.roi]]
			first_column = len(list(self.df))
			number_of_letters = sum(len(i) for i in list(self.df))
			width = number_of_letters + (first_column * 3)

			self.scroll = Scrollbar(root)
			self.scroll.pack(side=RIGHT, fill=Y)
			
			self.text1 = Text(root, height=20, width = width, wrap=NONE, yscrollcommand=self.scroll.set)
			self.text1.insert(END, self.df)
			self.text1.pack()

			statusbar['text'] = 'Calculations performed'
		except:
			messagebox.showinfo('Alert', 'Nothing to run calculations on. Please load a .csv')


	def graph(self):
		try:
			ax = plt.gca()
			self.df.plot(kind='line', x=self.date_of_sale, y=self.input_price, ax=ax)
			self.df.plot(kind='line', x=self.date_of_sale, y=self.roi, color='red', ax=ax)
			plt.show()
		except:
			messagebox.showinfo('Alert', 'Nothing to plot a graph on. Please load a .csv')
	

	

	

root = Tk()
root.title('A-Tool')
root.iconbitmap(r'assets\\icons\\main_icon.ico')
openButton_icon = PhotoImage(file='assets\\icons\\open.png')
saveButton_icon = PhotoImage(file='assets\\icons\\save_as.png')
helpButton_icon = PhotoImage(file='assets\\icons\\help.png')
calculationsButton_icon = PhotoImage(file='assets\\icons\\calculations.png')
graphButton_icon = PhotoImage(file='assets\\icons\\graph.png')
quitButton_icon = PhotoImage(file='assets\\icons\\exit.png')
root.geometry('600x400')
b = MainWindow(root)
root.mainloop()