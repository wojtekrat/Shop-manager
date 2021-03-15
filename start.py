from records import *
from tkinter import *


class Start:
    def __init__(self):
        self.root = Tk()
        self.root.title('Shop manager')
        self.root.geometry("650x295")
        self.root.resizable(False, False)
        self.db_name = Entry(self.root, width=60)
        self.db_name.grid(row=0, column=1, padx=50, pady=100)
        self.db_name_label = Label(self.root, text="Enter your database name: ")
        self.db_name_label.grid(row=0, column=0)
        self.db_button = Button(self.root, text="Create database", command=self.start_record)
        self.db_button.grid(row=1, columnspan=2, ipadx=180, ipady=20)

        self.db_title = self.db_name.get()

        self.root.mainloop()

    def get_dbname(self):
        self.db_title = self.db_name.get()

    def start_record(self):
        self.root.destroy()
        Records()

