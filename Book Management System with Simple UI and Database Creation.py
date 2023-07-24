import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("book.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS book (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            author TEXT,
                            price REAL)''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM book")
        rows = self.cur.fetchall()
        return rows

    def insert(self, book_id, book_title, book_price):
        self.cur.execute("INSERT INTO book (id, title, price) VALUES (?, ?, ?)",
                         (book_id, book_title, book_price,))
        self.conn.commit()

    def update(self, book_id, book_title, book_price):
        self.cur.execute("UPDATE book SET title=?, price=? WHERE id=?",
                         (book_title, book_price, book_id))
        self.conn.commit()

    def delete(self, book_id):
        self.cur.execute("DELETE FROM book WHERE id=?", (book_id,))
        self.conn.commit()

    def search(self, book_id="", book_title=""):
        query = "SELECT * FROM book WHERE 1=1"
        params = []

        if book_id:
            query += " AND id=?"
            params.append(book_id)
        if book_title:
            query += " AND title=?"
            params.append(book_title)

        self.cur.execute(query, tuple(params))

        rows = self.cur.fetchall()
        return rows

       
       
       
        
db = DB()

selected_tuple = ()

def get_selected_row(event):
    global selected_tuple
    try:
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[0])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[1])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[2])
    except IndexError:
        pass

def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)

def search_command():
    id_text = e1.get()
    title_text = e2.get()
    list1.delete(0, END)
    for row in db.search(id_text, title_text):
        list1.insert(END, row)

def add_command():
    book_id = e1.get()
    book_title = e2.get()
    book_price = e3.get()
    if not book_id or not book_title or not book_price:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    db.insert(book_id, book_title, book_price)
    view_command()

def delete_command():
    try:
        book_id = selected_tuple[0]
        db.delete(book_id)
        view_command()
    except IndexError:
        pass

def update_command():
    try:
        book_id = selected_tuple[0]
        book_title = e2.get()
        book_price = e3.get()
        if not book_title or not book_price:
            messagebox.showerror("Error", "Please enter book title and price.")
            return

        db.update(book_id, book_title, book_price)
        view_command()
    except IndexError:
        pass

window = Tk()
window.title("Book Management System")

window.iconbitmap("cmrit.ico")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

l1 = Label(window, text="Book_id")
l1.grid(row=0, column=0)

l2 = Label(window, text="Book_name")
l2.grid(row=1, column=0)

l3 = Label(window, text="Price")
l3.grid(row=2, column=0)

e1 = Entry(window)
e1.grid(row=0, column=1)

e2 = Entry(window)
e2.grid(row=1, column=1)

e3 = Entry(window)
e3.grid(row=2, column=1)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=3, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=3, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="View All", width=12, command=view_command)
b1.grid(row=3, column=3, pady=5)

b2 = Button(window, text="Search Entry", width=12, command=search_command)
b2.grid(row=4, column=3, pady=5)

b3 = Button(window, text="Add Entry", width=12, command=add_command)
b3.grid(row=5, column=3, pady=5)

b4 = Button(window, text="Update Selected", width=12, command=update_command)
b4.grid(row=6, column=3, pady=5)

b5 = Button(window, text="Delete Selected", width=12, command=delete_command)
b5.grid(row=7, column=3, pady=5)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=8, column=3, pady=5)

window.mainloop()
