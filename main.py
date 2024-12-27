from tkinter import *
import pymysql
from tkinter import messagebox

print(pymysql.__version__)

passwd = "tanish"
database = "library"
issueTable = "books_issued"
bookTable = "books"

con = pymysql.connect(host="localhost", user="root", password=passwd, database=database)
cur = con.cursor()


def book_register(bid, title, author):
    status_new = "Available"  # default status of a new book is Available

    if not bid or not title or not author:
        messagebox.showinfo("Error", "One or more fields are empty")

    else:
        insertBooks = f"insert into {bookTable} values('{bid}','{title}','{author}','{status_new}')"
        try:
            cur.execute(insertBooks)
            con.commit()
            messagebox.showinfo('Success', "Book added successfully")

        except pymysql.err.IntegrityError:
            messagebox.showinfo("Error", "Book ID already exists")

    root_add_book.destroy()


def add_book():
    global root_add_book

    root_add_book = Tk()
    root_add_book.title("Library - Add Book")
    root_add_book.minsize(width=400, height=400)
    root_add_book.geometry("600x500")

    Canvas1 = Canvas(root_add_book)

    Canvas1.config(bg="#445D48")
    Canvas1.pack(expand=True, fill=BOTH)

    heading_frame = Frame(root_add_book, bg="#FDE5D4", bd=5)
    heading_frame.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(heading_frame, text="Add a Book", bg='#D6CC99', fg='#001524', font=('Helvetica', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root_add_book, bg='#001524')
    labelFrame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.4)

    # Book ID
    lb1 = Label(labelFrame, text="Book ID : ", bg='#001524', fg='#FDE5D4', font=('Helvetica', 10))
    lb1.place(relx=0.05, rely=0.2, relheight=0.12)

    book_id = Entry(labelFrame)
    book_id.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.12)

    # Title
    lb2 = Label(labelFrame, text="Title : ", bg='#001524', fg='#FDE5D4', font=('Helvetica', 10))
    lb2.place(relx=0.05, rely=0.4, relheight=0.12)

    Title = Entry(labelFrame)
    Title.place(relx=0.3, rely=0.4, relwidth=0.62, relheight=0.12)

    # Book Author
    lb3 = Label(labelFrame, text="Author : ", bg='#001524', fg='#FDE5D4', font=('Helvetica', 10))
    lb3.place(relx=0.05, rely=0.6, relheight=0.12)

    Author = Entry(labelFrame)
    Author.place(relx=0.3, rely=0.6, relwidth=0.62, relheight=0.12)

    # Submit Button
    SubmitBtn = Button(root_add_book,
                       text="Submit",
                       bg='#D6CC99',
                       fg='black',
                       command=lambda: book_register(book_id.get(), Title.get(), Author.get()),
                       font=('Helvetica', 10))
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    QuitBtn = Button(root_add_book, text="Exit", bg='#D6CC99', fg='black', command=root_add_book.destroy, font=('Helvetica', 10))
    QuitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root_add_book.mainloop()


def delete_book(bid):
    try:
        cur.execute(f"SELECT 1 FROM {bookTable} WHERE bid = '{bid}'")
        bid_present = cur.fetchone()

        if bid_present:
            delete_main = f"delete from {bookTable} where bid = '{bid}'"
            delete_issue = f"delete from {issueTable} where bid = '{bid}'"
            cur.execute(delete_main)
            cur.execute(delete_issue)
            con.commit()
            messagebox.showinfo('Success', "Book record deleted successfully!")
        else:
            messagebox.showinfo('Error', "Book record not found")
    except Exception as e:
        messagebox.showinfo("Error", f"Could not delete book: {e}")

    root_delete_book.destroy()


def delete():
    global root_delete_book

    root_delete_book = Tk()
    root_delete_book.title("Library - Delete Book")
    root_delete_book.minsize(width=400, height=400)
    root_delete_book.geometry("600x500")

    Canvas1 = Canvas(root_delete_book)

    Canvas1.config(bg="#DC6D18")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root_delete_book, bg="#FFF4E4", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Delete Book", bg='#F8E0C9', fg='#2B1A12', font=('Helvetica', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root_delete_book, bg='#2B1A12')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Book ID to Delete
    lb2 = Label(labelFrame, text="Book ID : ", bg='#2B1A12', fg='#FFF4E4', font=('Helvetica', 10))
    lb2.place(relx=0.05, rely=0.5)

    book_id = Entry(labelFrame)
    book_id.place(relx=0.3, rely=0.5, relwidth=0.62, relheight=0.09)

    # Submit Button
    SubmitBtn = Button(root_delete_book,
                       text="SUBMIT",
                       bg='#F8E0C9',
                       fg='#2B1A12',
                       command=lambda: delete_book(book_id.get()),
                       font=('Helvetica', 10))
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root_delete_book, text="Quit", bg='#F8E0C9', fg='#2B1A12', command=root_delete_book.destroy, font=('Helvetica', 10))
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root_delete_book.mainloop()


def issue(bid, student_name, student_id, date):

    extractBid = f"SELECT * FROM {bookTable} WHERE bid = '{bid}'"
    cur.execute(extractBid)
    row = cur.fetchone()
    if row:
        status = (row[3] == 'Available')

    else:
        messagebox.showinfo("Error", "Book ID does not exist")
        root_issue_book.destroy()
        return

    try:
        if status:
            updateStatus = f"update {bookTable} set status = 'Issued' where bid = '{bid}'"
            issueSql = f"INSERT INTO {issueTable} values('{bid}', '{student_name}', '{student_id}', '{date}')"
            cur.execute(updateStatus)
            cur.execute(issueSql)
            con.commit()

            messagebox.showinfo('Success', "Book Issued Successfully")
            root_issue_book.destroy()
        else:
            messagebox.showinfo('Message', "Cannot Issue: Book Already Issued")
            root_issue_book.destroy()
    except Exception as e:
        messagebox.showinfo("Error", f"Could not issue book: {e}")


def issue_book():
    global root_issue_book

    root_issue_book = Tk()
    root_issue_book.title("Library - Issue a Book")
    root_issue_book.minsize(width=400, height=400)
    root_issue_book.geometry("600x500")

    Canvas1 = Canvas(root_issue_book)
    Canvas1.config(bg="#55356E")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root_issue_book, bg="#E9E2F3", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Issue Book", bg='#D6F5FF', fg='#191308', font=('Helvatica', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root_issue_book, bg='#191308')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Book ID
    lb1 = Label(labelFrame, text="Book ID: ", bg='#191308', fg='#E9E2F3', font=('Helvetica', 10))
    lb1.place(relx=0.05, rely=0.2)

    book_id = Entry(labelFrame)
    book_id.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.12)

    # Issued To Student name
    lb2 = Label(labelFrame, text="Student Name: ", bg='#191308', fg='#E9E2F3', font=('Helvetica', 10))
    lb2.place(relx=0.05, rely=0.4)

    s_name = Entry(labelFrame)
    s_name.place(relx=0.3, rely=0.4, relwidth=0.62, relheight=0.12)

    # Student ID
    lb3 = Label(labelFrame, text="Student ID: ", bg='#191308', fg='#E9E2F3', font=('Helvetica', 10))
    lb3.place(relx=0.05, rely=0.6)

    s_id = Entry(labelFrame)
    s_id.place(relx=0.3, rely=0.6, relwidth=0.62, relheight=0.12)

    # Date
    lb4 = Label(labelFrame, text="Date Issued On: ", bg='#191308', fg='#E9E2F3', font=('Helvetica', 10))
    lb4.place(relx=0.05, rely=0.8)

    date_of_issuing = Entry(labelFrame)
    date_of_issuing.place(relx=0.3, rely=0.8, relwidth=0.62, relheight=0.12)

    # Issue Button
    issueBtn = Button(root_issue_book,
                      text="Issue",
                      bg='#D6F5FF',
                      fg='#191308',
                      command=lambda: issue(book_id.get(), s_name.get(), s_id.get(), date_of_issuing.get()),
                      font=('Helvetica', 10))
    issueBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root_issue_book, text="Quit", bg='#D6F5FF', fg='#191308', command=root_issue_book.destroy, font=('Helvetica', 10))
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root_issue_book.mainloop()


def issued_books_list():
    root_issued_books_list = Tk()
    root_issued_books_list.title("Library - View Issued Books")
    root_issued_books_list.minsize(width=400, height=400)
    root_issued_books_list.geometry("600x500")

    Canvas1 = Canvas(root_issued_books_list)
    Canvas1.config(bg="#B9375E")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root_issued_books_list, bg="#FFE0E9", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Issued Books", bg='#CEDDBB', fg='#434343', font=('Helvetica', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root_issued_books_list, bg='#434343')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Add column headers
    headers = ['Book ID', 'Issued To', 'Student ID', 'Issue Date']
    for col, header in enumerate(headers):
        Label(labelFrame, text=header, bg='#434343', fg='#FFE0E9', font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=10, pady=5)

    getBooks = f"SELECT * FROM {issueTable}"
    try:
        cur.execute(getBooks)
        for row, data in enumerate(cur, start=1):
            for col, value in enumerate(data):
                Label(labelFrame, text=value, bg='#434343', fg='#FFE0E9', font=('Helvetica', 10)).grid(row=row, column=col, padx=10, pady=5)

    except Exception as e:
        messagebox.showinfo("Error", f"Failed to fetch files from database: {e}")

    quitBtn = Button(root_issued_books_list, text="Quit", bg='#CEDDBB', fg='#434343', command=root_issued_books_list.destroy)
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    root_issued_books_list.mainloop()


def returnn(bid):

    extractBid = f"SELECT * FROM {issueTable} WHERE bid = '{bid}'"
    cur.execute(extractBid)
    row = cur.fetchone()
    if not row:
        messagebox.showinfo("Error", "Book is not currently issued")
        root_return_book.destroy()
        return

    try:
        issueSql = f"delete from {issueTable} where bid = '{bid}'"
        updateStatus = f"update {bookTable} set status = 'Available' where bid = '{bid}'"
        cur.execute(issueSql)
        cur.execute(updateStatus)
        con.commit()
        messagebox.showinfo('Success', "Book returned successfully!")

    except Exception as e:
        messagebox.showinfo("Error", f"Failed to return book: {e}")

    root_return_book.destroy()


def return_book():
    global root_return_book

    root_return_book = Tk()
    root_return_book.title("Library - Return a Book")
    root_return_book.minsize(width=400, height=400)
    root_return_book.geometry("600x500")

    Canvas1 = Canvas(root_return_book)

    Canvas1.config(bg="#000000")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root_return_book, bg="#FBF4EF", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Return Book", bg='#AAABAE', fg='black', font=('Helvetica', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root_return_book, bg='#AAABAE')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Book ID to return
    lb1 = Label(labelFrame, text="Book ID : ", bg='#AAABAE', fg='black', font=('Helvetica', 10))
    lb1.place(relx=0.05, rely=0.5)

    book_id = Entry(labelFrame)
    book_id.place(relx=0.3, rely=0.5, relwidth=0.62, relheight=0.09)

    # Submit Button
    SubmitBtn = Button(root_return_book,
                       text="Return",
                       bg='#E8EAEB',
                       fg='black',
                       command=lambda: returnn(book_id.get()),
                       font=('Helvetica', 10))
    SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root_return_book, text="Quit", bg='#E8EAEB', fg='black', command=root_return_book.destroy, font=('Helvetica', 10))
    quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    root_return_book.mainloop()


def view():
    root_view_books = Tk()
    root_view_books.title("Library - View Books")
    root_view_books.minsize(width=400, height=400)
    root_view_books.geometry("600x500")

    Canvas1 = Canvas(root_view_books)
    Canvas1.config(bg="#A86A24")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root_view_books, bg="#FEFAE0", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Books", bg='#FFFFFF', fg='#151C0D', font=('Helvetica', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root_view_books, bg='#151C0D')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Add column headers
    headers = ['BID', 'Title', 'Author', 'Status']
    for col, header in enumerate(headers):
        Label(labelFrame, text=header, bg='#151C0D', fg='white', font=('Helvetica', 10, 'bold'), anchor='center').grid(row=0, column=col, padx=10, pady=5)

    getBooks = "SELECT * FROM " + bookTable
    try:
        cur.execute(getBooks)
        con.commit()
        for row, data in enumerate(cur, start=1):  # Start from row 1 as row 0 is for headers
            for col, value in enumerate(data):
                Label(labelFrame, text=value, bg='#151C0D', fg='white', font=('Helvetica', 10)).grid(row=row, column=col, padx=10, pady=5)

    except Exception as e:
        messagebox.showinfo("Error", f"Failed to fetch data from the database: {e}")

    quitBtn = Button(root_view_books, text="Quit", bg='white', fg='#151C0D', command=root_view_books.destroy)
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    root_view_books.mainloop()


def main():
    root = Tk()
    root.title("Library Management System")
    root.minsize(width=400, height=400)
    root.geometry("600x500")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#0274BD")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#C4AD9D", bd=5)
    headingFrame1.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Library Management System", bg='#E9E6DD', fg='black', font=('Helvetica', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    btn1 = Button(root, text="Add Book", bg='black', fg='#E9E6DD', command=add_book, font=('Helvetica', 10))
    btn1.place(relx=0.28, rely=0.25, relwidth=0.45, relheight=0.1)

    btn2 = Button(root, text="View All Books", bg='black', fg='#E9E6DD', command=view, font=('Helvetica', 10))
    btn2.place(relx=0.28, rely=0.35, relwidth=0.45, relheight=0.1)

    btn3 = Button(root, text="Delete Book", bg='black', fg='#E9E6DD', command=delete, font=('Helvetica', 10))
    btn3.place(relx=0.28, rely=0.45, relwidth=0.45, relheight=0.1)

    btn4 = Button(root, text="Issue Book", bg='black', fg='#E9E6DD', command=issue_book, font=('Helvetica', 10))
    btn4.place(relx=0.28, rely=0.55, relwidth=0.45, relheight=0.1)

    btn5 = Button(root, text="Issued Books", bg='black', fg='#E9E6DD', command=issued_books_list, font=('Helvetica', 10))
    btn5.place(relx=0.28, rely=0.65, relwidth=0.45, relheight=0.1)

    btn6 = Button(root, text="Return Book", bg='black', fg='#E9E6DD', command=return_book, font=('Helvetica', 10))
    btn6.place(relx=0.28, rely=0.75, relwidth=0.45, relheight=0.1)

    quitBtn = Button(root, text="Exit", bg='#E9E6DD', fg='black', command=root.destroy, font=('Helvetica', 10))
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()


if __name__ == "__main__":
    main()
