from tkinter import messagebox
import sqlite3
from tkinter import *


class Records:

    def __init__(self):
        from start import Start
        self.title = Start.get_dbname()
        self.root = Tk()
        self.root.title('Shop manager')
        self.root.geometry("615x400")
        self.root.resizable(False, False)

        self.store_id = Entry(self.root, width=30)
        self.store_id.grid(row=0, column=1, pady=(10, 0))
        self.name = Entry(self.root, width=30)
        self.name.grid(row=1, column=1)
        self.price = Entry(self.root, width=30)
        self.price.grid(row=2, column=1)

        self.store_label = Label(self.root, text="ITEM ID:")
        self.store_label.grid(row=0, column=0, pady=(10, 0))
        self.name_label = Label(self.root, text="NAME:")
        self.name_label.grid(row=1, column=0)
        self.price_label = Label(self.root, text="PRICE:")
        self.price_label.grid(row=2, column=0)

        self.store_id2 = Entry(self.root, width=30)
        self.store_id2.grid(row=0, column=3, pady=(10, 0))
        self.name2 = Entry(self.root, width=30)
        self.name2.grid(row=1, column=3)
        self.price2 = Entry(self.root, width=30)
        self.price2.grid(row=2, column=3)

        self.store_label2 = Label(self.root, text="ITEM ID:")
        self.store_label2.grid(row=0, column=2, pady=(10, 0))
        self.name_label2 = Label(self.root, text="NAME:")
        self.name_label2.grid(row=1, column=2)
        self.price_label2 = Label(self.root, text="PRICE:")
        self.price_label2.grid(row=2, column=2)

        self.submit_btn = Button(self.root, text="Add record to database", command=self.submit)
        self.submit_btn.grid(row=6, column=0, columnspan=2, pady=2, padx=10, ipadx=110)

        self.query_btn = Button(self.root, text="Show record", command=self.query)
        self.query_btn.grid(row=7, column=0, columnspan=2, pady=2, padx=10, ipadx=139)

        self.delete_btn = Button(self.root, text="Delete record", command=self.delete)
        self.delete_btn.grid(row=8, column=0, columnspan=2, pady=2, padx=10, ipadx=138)

        self.edit_btn = Button(self.root, text="Edit record", command=self.edit)
        self.edit_btn.grid(row=9, column=0, columnspan=2, pady=2, padx=10, ipadx=145)

        self.update_btn = Button(self.root, text="Save record", command=self.update)
        self.update_btn.grid(row=10, column=0, columnspan=2, pady=2, padx=10, ipadx=143)

        self.show_all_btn = Button(self.root, text="Show all records", command=self.show)
        self.show_all_btn.grid(row=11, column=0, columnspan=2, pady=2, padx=10, ipadx=130)

        self.status = Label(self.root, text="sadasd", bd=1, relief=SUNKEN, anchor=E)
        self.status.grid(row=12, sticky=EW, pady=120, columnspan=6)

        self.store_num = self.store_id.get()
        self.store_name = self.name.get()
        self.store_price = self.price.get()
        self.records = []

        self.conn = sqlite3.connect(str(self.title) + '.db')
        self.cursor = self.conn.cursor()

        self.command1 = '''CREATE TABLE IF NOT EXISTS
        purchases(store_id INTEGER PRIMARY KEY, name TEXT, total_cost FLOAT)'''

        self.cursor.execute(self.command1)
        self.status["text"] = "Table created successfully"

        self.conn.commit()
        self.conn.close()

    def clear(self):
        self.store_id.delete(0, END)
        self.name.delete(0, END)
        self.price.delete(0, END)
        self.status["text"] = ""

    def show(self):
        return

    def update(self):
        self.store_num = self.store_id.get()
        dig = str(self.store_num).isdigit()
        if self.store_num == "" or not dig:
            messagebox.showwarning("Warning", "Please enter a valid item id")
        else:
            self.conn = sqlite3.connect(str(self.title) + '.db')
            self.cursor = self.conn.cursor()
            self.store_num = self.store_id.get()
            self.store_name = self.name.get()
            self.store_price = self.price.get()
            self.records = [int(self.store_num), str(self.store_name), float(self.store_price)]
            self.cursor.execute("""UPDATE purchases SET 
                                        store_id = :store,
                                        name = :name,
                                        total_cost = :total_cost

                                        WHERE oid = :oid""",
                                {
                                    'store': self.store_num,
                                    'name': self.store_name,
                                    'total_cost': self.store_price,
                                    'oid': self.store_num
                                })

            self.conn.commit()
            self.conn.close()

            self.clear()
            self.status["text"] = "Record updated successfully"

    def edit(self):
        self.store_num = self.store_id.get()
        dig = str(self.store_num).isdigit()
        if self.store_num == "" or not dig:
            messagebox.showwarning("Warning", "Please enter a valid item id")
        else:
            self.conn = sqlite3.connect(str(self.title) + '.db')
            self.cursor = self.conn.cursor()
            self.store_num = self.store_id.get()
            self.cursor.execute("SELECT * FROM purchases WHERE oid = " + self.store_num)
            self.store_id.delete(0, END)
            result = self.cursor.fetchall()
            self.clear()

            for x in result:
                self.store_id.insert(0, x[0])
                self.name.insert(0, x[1])
                self.price.insert(0, x[2])

    def delete(self):
        self.conn = sqlite3.connect(str(self.title) + '.db')
        self.cursor = self.conn.cursor()
        self.store_num = self.store_id.get()
        self.cursor.execute("DELETE from purchases WHERE oid=" + self.store_num)
        self.conn.commit()
        self.conn.close()
        self.status["text"] = "Record deleted successfully"
        self.store_id.delete(0, END)

    def submit(self):
        self.conn = sqlite3.connect(str(self.title) + '.db')
        self.cursor = self.conn.cursor()
        self.store_num = self.store_id.get()
        self.store_name = self.name.get()
        self.store_price = self.price.get()
        self.records = [int(self.store_num), str(self.store_name), float(self.store_price)]
        self.cursor.execute("INSERT INTO purchases VALUES (?,?,?) ;", self.records)
        print("Added successfully")
        self.conn.commit()
        self.conn.close()
        self.clear()
        self.status["text"] = "Record added successfully"

    def query(self):
        self.store_id2.delete(0, END)
        self.name2.delete(0, END)
        self.price2.delete(0, END)
        self.store_num = self.store_id.get()
        dig = str(self.store_num).isdigit()
        if self.store_num == "" or not dig:
            messagebox.showwarning("Warning", "Please enter a valid item id")
        else:
            self.conn = sqlite3.connect(str(self.title) + '.db')
            self.cursor = self.conn.cursor()
            self.store_num = self.store_id.get()
            self.cursor.execute("SELECT * FROM purchases WHERE oid = " + self.store_num)
            self.store_id.delete(0, END)
            result = self.cursor.fetchall()
            for x in result:
                self.store_id2.insert(END, str(x[0]))
                self.name2.insert(END, str(x[1]))
                self.price2.insert(END, str(x[2]))
            self.conn.commit()
            self.conn.close()
            self.clear()
