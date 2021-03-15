from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import filedialog


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title('Shop manager')
        self.root.geometry("560x295")
        self.root.resizable(False, False)
        self.db_name = Entry(self.root, width=60)
        self.db_name.grid(row=0, column=1, padx=(10, 50), pady=(100, 30))
        self.db_name_label = Label(self.root, text="Enter your database name: ")
        self.db_name_label.grid(row=0, column=0, pady=(70, 0), padx=(10, 2))
        self.db_button = Button(self.root, text="Create/Open database", command=self.get_dbname)
        self.db_button.grid(row=1, columnspan=2, ipadx=50)
        self.open_button = Button(self.root, text="Open database from folder", command=self.open_file)
        self.open_button.grid(row=2, columnspan=2, ipadx=38)

        self.db_title = self.db_name.get()
        self.root.mainloop()

    def get_dbname(self):
        self.db_title = str(self.db_name.get() + ".db")
        self.Records(self.db_title)
        self.root.destroy()

    def open_file(self):
        self.root.filename = filedialog.askopenfilename(filetypes=(("db files", "*.db"), ("all files", "*.*")))
        self.db_title = self.root.filename
        if self.db_title != "":
            self.Records(self.db_title)
            self.root.destroy()
        else:
            self.root.destroy()
            App()

    class Records:
        def __init__(self, db_name):
            self.title = db_name
            self.root = Tk()
            self.root.title('Shop manager')
            self.root.geometry("320x390")
            self.root.resizable(False, False)

            self.menubar = Menu(self.root)
            self.recordmenu = Menu(self.menubar)
            self.recordmenu.add_command(label="Add new", command=lambda: App.Submit(self.title))
            self.recordmenu.add_command(label="Edit", command=self.edit)
            self.recordmenu.add_command(label="Delete", command=self.delete)
            self.recordmenu.add_command(label="Show all", command=lambda: App.ShowAll(self.title))

            self.filemenu = Menu(self.menubar)
            self.filemenu.add_command(label="Open", command=self.open_new)
            self.filemenu.add_command(label="Exit", command=lambda: self.root.destroy())

            self.menubar.add_cascade(label="File", menu=self.filemenu)
            self.menubar.add_cascade(label="Record", menu=self.recordmenu)

            self.root.config(menu=self.menubar)

            self.find_frame = Frame(self.root)
            self.find_frame.grid(row=0, column=0, columnspan=2)

            self.record_frame = Frame(self.root)
            self.record_frame.grid(row=1, column=0)

            self.item_id_label = Label(self.find_frame, text="Find item:")
            self.item_id_label.grid(row=0, column=0, pady=(50, 0), padx=10)
            self.item_id = Entry(self.find_frame, width=35)
            self.item_id.grid(row=0, column=1, pady=(50, 0), padx=1)

            self.query_btn = Button(self.find_frame, text="FIND ITEM", command=self.find, width=30)
            self.query_btn.grid(row=1, column=0, columnspan=2, pady=(15, 50), padx=10)

            self.store_id = Entry(self.record_frame, width=30, state=DISABLED)
            self.store_id.grid(row=3, column=1, sticky=W, padx=2)
            self.name = Entry(self.record_frame, width=30, state=DISABLED)
            self.name.grid(row=4, column=1, sticky=W, padx=2)
            self.price = Entry(self.record_frame, width=30, state=DISABLED)
            self.price.grid(row=5, column=1, sticky=W, padx=2)

            self.store_label2 = Label(self.record_frame, text="ITEM ID:")
            self.store_label2.grid(row=3, column=0, padx=2)
            self.name_label2 = Label(self.record_frame, text="NAME:")
            self.name_label2.grid(row=4, column=0, padx=2)
            self.price_label2 = Label(self.record_frame, text="PRICE:")
            self.price_label2.grid(row=5, column=0, padx=2)

            self.delete_btn = Button(self.record_frame, text="Delete record", command=self.delete)
            self.delete_btn.grid(row=6, column=1, sticky=W, padx=2, ipadx=3, pady=(2, 0))

            self.edit_btn = Button(self.record_frame, text="Edit record", command=self.edit)
            self.edit_btn.grid(row=6, column=1, sticky=E, padx=2, ipadx=14, pady=(2, 0))

            self.store_num = self.item_id.get()
            self.store_name = self.name.get()
            self.store_price = self.price.get()
            self.records = []

            self.conn = sqlite3.connect(str(self.title))
            self.cursor = self.conn.cursor()

            self.command1 = '''CREATE TABLE IF NOT EXISTS
                    purchases(store_id INTEGER PRIMARY KEY, name TEXT, total_cost FLOAT)'''

            self.cursor.execute(self.command1)

            App.StatusBar(f"DB has loaded successfully: {self.title}", self.root)

            self.conn.commit()
            self.conn.close()

        def open_new(self):
            self.root.destroy()
            App()

        def entry_activate(self):
            self.store_id["state"] = NORMAL
            self.price["state"] = NORMAL
            self.name["state"] = NORMAL

        def entry_deactivate(self):
            self.store_id["state"] = DISABLED
            self.name["state"] = DISABLED
            self.price["state"] = DISABLED

        def clear(self):
            self.item_id.delete(0, END)
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.store_id.delete(0, END)

        def edit(self):
            self.store_num = self.store_id.get()
            if self.store_num == "":
                App.MessageBox("Empty record", "Can't edit an empty record")
            else:
                App.Edit(self.store_num, self.title)

        def delete(self):
            self.store_num = self.store_id.get()
            if self.store_num == "":
                App.MessageBox("Empty record", "Record is empty, can't delete")
            else:
                self.entry_activate()
                self.conn = sqlite3.connect(str(self.title))
                self.cursor = self.conn.cursor()
                self.cursor.execute("DELETE from purchases WHERE oid=" + self.store_num)
                self.conn.commit()
                self.conn.close()
                App.MessageBox("Record deleted", "Record has been deleted from database")
                self.clear()
                self.entry_deactivate()

        def find(self):
            self.store_id.delete(0, END)
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.store_num = self.item_id.get()
            dig = str(self.store_num).isdigit()
            if self.store_num == "":
                App.MessageBox("Enter Item ID", "Enter an item ID")
            elif not dig:
                App.MessageBox("Enter valid ID", "Enter valid item ID, must be integer")
            else:
                self.entry_activate()
                self.conn = sqlite3.connect(str(self.title))
                self.cursor = self.conn.cursor()
                self.store_num = self.item_id.get()
                self.cursor.execute("SELECT * FROM purchases WHERE store_id = " + self.store_num)
                self.clear()
                result = self.cursor.fetchall()
                if len(result) == 0:
                    App.MessageBox("Invalid ID", "There is no such item ID")
                else:
                    for x in result:
                        self.store_id.insert(END, str(x[0]))
                        self.name.insert(END, str(x[1]))
                        self.price.insert(END, str(x[2]))
                self.conn.commit()
                self.conn.close()
                self.entry_deactivate()

    class Edit:
        def __init__(self, store_num, db_name):
            self.root2 = Tk()
            self.root2.title('Edit record')
            self.root2.geometry("250x150")
            self.root2.resizable(False, False)
            self.store_num = store_num

            self.store_id1 = Entry(self.root2, width=30)
            self.store_id1.grid(row=0, column=1, pady=(10, 0))
            self.name1 = Entry(self.root2, width=30)
            self.name1.grid(row=1, column=1)
            self.price1 = Entry(self.root2, width=30)
            self.price1.grid(row=2, column=1)

            self.store_label1 = Label(self.root2, text="ITEM ID:")
            self.store_label1.grid(row=0, column=0, pady=(10, 0), padx=(5, 2))
            self.name_label1 = Label(self.root2, text="NAME:")
            self.name_label1.grid(row=1, column=0, padx=(5, 2))
            self.price_label1 = Label(self.root2, text="PRICE:")
            self.price_label1.grid(row=2, column=0, padx=(5, 2))

            self.update_btn = Button(self.root2, text="Save record", command=self.update)
            self.update_btn.grid(row=3, column=0, columnspan=2, pady=10)

            self.title = db_name

            self.conn = sqlite3.connect(str(self.title))
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM purchases WHERE store_id = " + self.store_num)
            self.result = self.cursor.fetchall()

            for x in self.result:
                self.store_id1.insert(0, x[0])
                self.name1.insert(0, x[1])
                self.price1.insert(0, x[2])

            self.conn.commit()
            self.conn.close()

        def update(self):
            self.conn = sqlite3.connect(str(self.title))
            dig = str(self.store_num).isdigit()
            if self.store_num == "" or not dig:
                App.MessageBox("Wrong value", "Type an item ID")
            else:
                store_name = self.name1.get()
                store_price = self.price1.get()
                self.conn = sqlite3.connect(str(self.title))
                self.cursor = self.conn.cursor()
                self.cursor.execute("""UPDATE purchases SET 
                                                        store_id = :store,
                                                        name = :name,
                                                        total_cost = :total_cost
    
                                                        WHERE oid = :oid""",
                                    {
                                        'store': self.store_num,
                                        'name': store_name,
                                        'total_cost': store_price,
                                        'oid': self.store_num
                                    })

                self.conn.commit()
                self.conn.close()
                App.MessageBox("Record updated", "Record has been updated")
                self.root2.destroy()

    class Submit:
        def __init__(self, db_name):
            self.root3 = Tk()
            self.root3.title('Add new')
            self.root3.geometry("250x150")
            self.root3.resizable(False, False)
            self.title = db_name

            self.store_id1 = Entry(self.root3, width=30)
            self.store_id1.grid(row=0, column=1, pady=(10, 0))
            self.name1 = Entry(self.root3, width=30)
            self.name1.grid(row=1, column=1)
            self.price1 = Entry(self.root3, width=30)
            self.price1.grid(row=2, column=1)

            self.store_label1 = Label(self.root3, text="ITEM ID:")
            self.store_label1.grid(row=0, column=0, pady=(10, 0), padx=(5, 2))
            self.name_label1 = Label(self.root3, text="NAME:")
            self.name_label1.grid(row=1, column=0, padx=(5, 2))
            self.price_label1 = Label(self.root3, text="PRICE:")
            self.price_label1.grid(row=2, column=0, padx=(5, 2))

            self.submit_btn = Button(self.root3, text="Save new record", command=self.submit)
            self.submit_btn.grid(row=3, column=0, columnspan=2, pady=10)

        def submit(self):
            store_num = self.store_id1.get()
            store_name = self.name1.get()
            store_price = self.price1.get()
            conn = sqlite3.connect(str(self.title))
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM purchases WHERE oid = " + store_num)
            data = cursor.fetchall()
            if len(data) == 0:
                records = [int(store_num), str(store_name), float(store_price)]
                cursor.execute("INSERT INTO purchases VALUES (?,?,?) ;", records)
                conn.commit()
                conn.close()
                App.MessageBox("Record added", "Record added to database")
                self.root3.destroy()
            else:
                App.MessageBox("Duplicate", "Record already exists")
                self.root3.destroy()

    class ShowAll:
        def __init__(self, db_name):
            self.title = db_name
            self.conn = sqlite3.connect(str(self.title))
            self.r_set = self.conn.execute("SELECT count(*) as no from purchases")
            self.data_row = self.r_set.fetchone()
            self.no_rec = self.data_row[0]
            self.limit = 20

            if self.data_row[0] > 0:
                self.new_w = Tk()
                self.new_w.title('Shop manager')
                self.new_w.geometry("290x450")
                self.new_w.resizable(False, False)
                self.label_id = Label(self.new_w, text="ITEM ID")
                self.label_id.grid(row=0, column=0)
                self.label_name = Label(self.new_w, text="NAME")
                self.label_name.grid(row=0, column=1)
                self.label_price = Label(self.new_w, text="PRICE")
                self.label_price.grid(row=0, column=2)
                self.show_all(0)
            else:
                App.MessageBox("Empty table", "Empty table, no records")

        def show_all(self, offset):

            q = "SELECT * from purchases LIMIT " + str(offset) + "," + str(self.limit)
            self.r_set = self.conn.execute(q)
            i = 0
            for record in self.r_set:
                for j in range(len(record)):
                    e = Entry(self.new_w, width=15)
                    e.grid(row=i + 1, column=j)
                    e.insert(END, record[j])
                i += 1
            while i < self.limit:
                for j in range(len(record)):
                    e = Entry(self.new_w, width=15)
                    e.grid(row=i + 1, column=j)
                    e.insert(END, "")
                i += 1

            back = offset - self.limit
            next = offset + self.limit
            next_btn = Button(self.new_w, text='Next >', command=lambda: self.show_all(next))
            next_btn.grid(row=21, column=2, pady=(10, 0))
            prev_btn = Button(self.new_w, text='< Prev', command=lambda: self.show_all(back))
            prev_btn.grid(row=21, column=0, pady=(10, 0))
            if self.no_rec <= next:
                next_btn["state"] = "disabled"
            else:
                next_btn["state"] = "active"

            if back >= 0:
                prev_btn["state"] = "active"
            else:
                prev_btn["state"] = "disabled"

            self.new_w.mainloop()

    class MessageBox:
        def __init__(self, title, text):
            self.root = Tk()
            self.root.withdraw()
            self.title = title
            self.text = text
            messagebox.showinfo(title, text)
            self.root.destroy()

    class StatusBar:
        def __init__(self, status_text, master):
            self.status_text = status_text
            self.status = Label(master, text=self.status_text, bd=1, relief=SUNKEN, anchor=E)
            self.status.grid(row=3, column=0, sticky=EW, pady=(115, 0), columnspan=3, ipadx=65)


obj = App()

