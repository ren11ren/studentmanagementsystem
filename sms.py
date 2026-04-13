from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime


# Global variables for database connection
db_connection = None
db_cursor = None


def connect_database():
    def connect():
        global db_connection, db_cursor
        try:
            db_connection = pymysql.connect(
                host=hostEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get(),
                charset='utf8mb4'
            )
            db_cursor = db_connection.cursor()

            db_cursor.execute(
                'create database if not exists studentmanagementsystem')

            db_cursor.execute('use studentmanagementsystem')

            db_cursor.execute('''
                create table if not exists students (
                    id int auto_increment primary key,
                    name varchar(100),
                    mobile varchar(15),
                    email varchar(100),
                    address varchar(200),
                    gender varchar(10),
                    dob varchar(20),
                    added_date varchar(20),
                    added_time varchar(20)
                )
            ''')

            messagebox.showinfo(
                'Success', 'Connection is successful', parent=connnectwindow)

            addstudentbutton.config(state=NORMAL, bg='#27ae60', fg='white')
            searchstudentbutton.config(state=NORMAL, bg='#2980b9', fg='white')
            deletestudentbutton.config(state=NORMAL, bg='#e74c3c', fg='white')
            updatestudentbutton.config(state=NORMAL, bg='#f39c12', fg='white')
            showstudentbutton.config(state=NORMAL, bg='#3498db', fg='white')
            exportbuttton.config(state=NORMAL, bg='#1abc9c', fg='white')

            connnectwindow.destroy()

            show_students()

        except Exception as e:
            messagebox.showerror(
                'Error', f'Connection failed:\n{str(e)}', parent=connnectwindow)

    connnectwindow = Toplevel()
    connnectwindow.geometry('450x300+500+200')
    connnectwindow.title('Connect To Database')
    connnectwindow.resizable(False, False)
    connnectwindow.configure(bg='#2c3e50')

    hostLabel = Label(connnectwindow, text='Host',
                      font=('times new roman', 18, 'bold'), bg='#2c3e50', fg='white')
    hostLabel.grid(row=0, column=0, pady=15, padx=20)
    hostEntry = Entry(connnectwindow, font=(
        'times new roman', 16, 'bold'), bd=3, relief=GROOVE, width=18)
    hostEntry.grid(row=0, column=1, pady=15, padx=15)
    hostEntry.insert(0, 'localhost')

    usernameLabel = Label(connnectwindow, text='Username',
                          font=('times new roman', 18, 'bold'), bg='#2c3e50', fg='white')
    usernameLabel.grid(row=1, column=0, pady=15, padx=20)
    usernameEntry = Entry(connnectwindow, font=(
        'times new roman', 16, 'bold'), bd=3, relief=GROOVE, width=18)
    usernameEntry.grid(row=1, column=1, pady=15, padx=15)
    usernameEntry.insert(0, 'root')

    passwordLabel = Label(connnectwindow, text='Password',
                          font=('times new roman', 18, 'bold'), bg='#2c3e50', fg='white')
    passwordLabel.grid(row=2, column=0, pady=15, padx=20)
    passwordEntry = Entry(connnectwindow, font=(
        'times new roman', 16, 'bold'), bd=3, relief=GROOVE, show='*', width=18)
    passwordEntry.grid(row=2, column=1, pady=15, padx=15)
    passwordEntry.insert(0, '')

    connectbutton = Button(connnectwindow, text='Connect', command=connect, width=12, font=(
        'times new roman', 14, 'bold'), bg='#27ae60', fg='white', bd=0, cursor='hand2')
    connectbutton.grid(row=3, column=1, pady=20)


def show_students():
    global db_cursor

    for item in studenttable.get_children():
        studenttable.delete(item)

    try:
        db_cursor.execute(
            "SELECT id, name, mobile, email, address, gender, dob, added_date, added_time FROM students")
        for row in db_cursor.fetchall():
            studenttable.insert("", END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load students: {str(e)}")


def add_student():
    if not db_connection:
        messagebox.showwarning("Warning", "Please connect to database first!")
        return

    dialog = Toplevel()
    dialog.title("Add Student")
    dialog.geometry("450x550")
    dialog.configure(bg='#ecf0f1')
    dialog.resizable(False, False)

    Label(dialog, text="Add New Student", font=('times new roman',
          20, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(pady=15)

    fields = ['Name', 'Mobile', 'Email',
              'Address', 'Gender', 'DOB (YYYY-MM-DD)']
    entries = {}

    frame = Frame(dialog, bg='#ecf0f1')
    frame.pack(pady=10)

    for i, field in enumerate(fields):
        Label(frame, text=field, bg='#ecf0f1', font=('times new roman', 12, 'bold'), fg='#34495e').grid(
            row=i, column=0, padx=15, pady=12, sticky=W)
        entry = Entry(frame, width=28, font=(
            'times new roman', 11), bd=2, relief=GROOVE)
        entry.grid(row=i, column=1, padx=15, pady=12)
        entries[field] = entry

    def save():
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')

        try:
            query = "INSERT INTO students (name, mobile, email, address, gender, dob, added_date, added_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
                entries['Name'].get(),
                entries['Mobile'].get(),
                entries['Email'].get(),
                entries['Address'].get(),
                entries['Gender'].get(),
                entries['DOB (YYYY-MM-DD)'].get(),
                current_date,
                current_time
            )
            db_cursor.execute(query, values)
            db_connection.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            dialog.destroy()
            show_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")

    Button(dialog, text="Save Student", command=save, bg='#27ae60', fg='white', font=(
        'times new roman', 12, 'bold'), width=15, bd=0, cursor='hand2').pack(pady=20)


def search_student():
    if not db_connection:
        messagebox.showwarning("Warning", "Please connect to database first!")
        return

    dialog = Toplevel()
    dialog.title("Search Student")
    dialog.geometry("450x180")
    dialog.configure(bg='#ecf0f1')
    dialog.resizable(False, False)

    Label(dialog, text="Search Student", font=('times new roman',
          18, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(pady=15)

    frame = Frame(dialog, bg='#ecf0f1')
    frame.pack(pady=10)

    Label(frame, text="Enter Name or Email:", bg='#ecf0f1', font=(
        'times new roman', 12, 'bold')).pack(side=LEFT, padx=10)
    search_entry = Entry(frame, width=25, font=(
        'times new roman', 11), bd=2, relief=GROOVE)
    search_entry.pack(side=LEFT, padx=10)

    def perform_search():
        term = search_entry.get()
        if not term:
            messagebox.showwarning("Warning", "Please enter search term!")
            return

        for item in studenttable.get_children():
            studenttable.delete(item)

        try:
            query = "SELECT * FROM students WHERE name LIKE %s OR email LIKE %s"
            db_cursor.execute(query, (f'%{term}%', f'%{term}%'))
            results = db_cursor.fetchall()
            for row in results:
                studenttable.insert("", END, values=row)

            dialog.destroy()
            messagebox.showinfo(
                "Search Results", f"Found {len(results)} student(s)")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    Button(dialog, text="Search", command=perform_search, bg='#3498db', fg='white', font=(
        'times new roman', 11, 'bold'), width=12, bd=0, cursor='hand2').pack(pady=15)


def delete_student():
    if not db_connection:
        messagebox.showwarning("Warning", "Please connect to database first!")
        return

    selected = studenttable.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student to delete!")
        return

    student_id = studenttable.item(selected[0])['values'][0]

    if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
        try:
            db_cursor.execute(
                "DELETE FROM students WHERE id = %s", (student_id,))
            db_connection.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            show_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {str(e)}")


def update_student():
    if not db_connection:
        messagebox.showwarning("Warning", "Please connect to database first!")
        return

    selected = studenttable.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student to update!")
        return

    student = studenttable.item(selected[0])['values']

    dialog = Toplevel()
    dialog.title("Update Student")
    dialog.geometry("450x550")
    dialog.configure(bg='#ecf0f1')
    dialog.resizable(False, False)

    Label(dialog, text="Update Student", font=('times new roman',
          20, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(pady=15)

    fields = ['Name', 'Mobile', 'Email',
              'Address', 'Gender', 'DOB (YYYY-MM-DD)']
    entries = {}

    frame = Frame(dialog, bg='#ecf0f1')
    frame.pack(pady=10)

    for i, field in enumerate(fields):
        Label(frame, text=field, bg='#ecf0f1', font=('times new roman', 12, 'bold'), fg='#34495e').grid(
            row=i, column=0, padx=15, pady=12, sticky=W)
        entry = Entry(frame, width=28, font=(
            'times new roman', 11), bd=2, relief=GROOVE)
        entry.grid(row=i, column=1, padx=15, pady=12)
        entry.insert(0, student[i+1])
        entries[field] = entry

    def save_update():
        try:
            query = "UPDATE students SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s WHERE id=%s"
            values = (
                entries['Name'].get(),
                entries['Mobile'].get(),
                entries['Email'].get(),
                entries['Address'].get(),
                entries['Gender'].get(),
                entries['DOB (YYYY-MM-DD)'].get(),
                student[0]
            )
            db_cursor.execute(query, values)
            db_connection.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            dialog.destroy()
            show_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")

    Button(dialog, text="Update Student", command=save_update, bg='#f39c12', fg='white', font=(
        'times new roman', 12, 'bold'), width=15, bd=0, cursor='hand2').pack(pady=20)


def export_data():
    if not db_connection:
        messagebox.showwarning("Warning", "Please connect to database first!")
        return

    try:
        import csv
        db_cursor.execute("SELECT * FROM students")
        data = db_cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No students to export!")
            return

        filename = f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Mobile', 'Email', 'Address',
                            'Gender', 'DOB', 'Added Date', 'Added Time'])
            writer.writerows(data)

        messagebox.showinfo("Success", f"Data exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {str(e)}")


def slider():
    # Keep the label text static (do not blink)
    sliderlabel.config(text='Student Management System')


def clock():
    date = datetime.now().strftime('%d-%m-%Y')
    currenttime = datetime.now().strftime('%H:%M:%S')
    datetimelabel.config(text=f'Date {date}\nTime: {currenttime}')
    datetimelabel.after(1000, clock)


root = Tk()
root.geometry('1200x700+0+0')
root.resizable(False, False)
root.title('Student Management System')
root.configure(bg='#ecf0f1')

datetimelabel = Label(root, text='Date and Time', font=(
    'times new roman', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50', bd=2, relief=GROOVE)
datetimelabel.place(x=10, y=10)
clock()

sliderlabel = Label(root, text='Student Management System', font=(
    'times new roman', 28, 'bold'), bg='#ecf0f1', fg="#151a1d")
sliderlabel.place(x=380, y=15)
slider()

connectbutton = Button(root, text='Connect Database', command=connect_database, bg='#27ae60',
                       fg='white', font=('times new roman', 12, 'bold'), bd=0, cursor='hand2', padx=15)
connectbutton.place(x=1040, y=12)

leftframe = Frame(root, bg='#2c3e50', bd=0, relief=FLAT)
leftframe.place(x=10, y=90, width=300, height=600)

try:
    logoimage = PhotoImage(file='std.png')
    logolabel = Label(leftframe, image=logoimage, bg='#2c3e50')
    logolabel.grid(row=0, column=0, pady=25)
except:
    logolabel = Label(leftframe, text='Student\nManagement', font=(
        'times new roman', 20, 'bold'), bg='#2c3e50', fg='white', width=15, height=3)
    logolabel.grid(row=0, column=0, pady=25)

addstudentbutton = Button(leftframe, text='Add Student', width=22, state=DISABLED, command=add_student,
                          bg='#34495e', fg='white', font=('times new roman', 11, 'bold'), bd=0, cursor='hand2', pady=8)
addstudentbutton.grid(row=1, column=0, pady=8)

searchstudentbutton = Button(leftframe, text='Search Student', width=22, state=DISABLED, command=search_student,
                             bg='#34495e', fg='white', font=('times new roman', 11, 'bold'), bd=0, cursor='hand2', pady=8)
searchstudentbutton.grid(row=2, column=0, pady=8)

deletestudentbutton = Button(leftframe, text='Delete Student', width=22, state=DISABLED, command=delete_student,
                             bg='#34495e', fg='white', font=('times new roman', 11, 'bold'), bd=0, cursor='hand2', pady=8)
deletestudentbutton.grid(row=3, column=0, pady=8)

updatestudentbutton = Button(leftframe, text='Update Student', width=22, state=DISABLED, command=update_student,
                             bg='#34495e', fg='white', font=('times new roman', 11, 'bold'), bd=0, cursor='hand2', pady=8)
updatestudentbutton.grid(row=4, column=0, pady=8)

showstudentbutton = Button(leftframe, text='Show Students', width=22, state=DISABLED, command=show_students,
                           bg='#34495e', fg='white', font=('times new roman', 11, 'bold'), bd=0, cursor='hand2', pady=8)
showstudentbutton.grid(row=5, column=0, pady=8)

exportbuttton = Button(leftframe, text='Export Data CSV', width=22, state=DISABLED, command=export_data,
                       bg='#34495e', fg='white', font=('times new roman', 11, 'bold'), bd=0, cursor='hand2', pady=8)
exportbuttton.grid(row=6, column=0, pady=8)

exitbutton = Button(leftframe, text='Exit', width=22, command=root.destroy, bg='#e74c3c',
                    fg='white', font=('times new roman', 11, 'bold'), bd=0, cursor='hand2', pady=8)
exitbutton.grid(row=7, column=0, pady=8)

rightframe = Frame(root, bg='white', bd=2, relief=GROOVE)
rightframe.place(x=330, y=90, width=860, height=600)

Scrollbarx = Scrollbar(rightframe, orient=HORIZONTAL)
Scrollbary = Scrollbar(rightframe, orient=VERTICAL)

style = ttk.Style()
style.configure("Treeview", font=('times new roman', 10), rowheight=28)
style.configure("Treeview.Heading", font=('times new roman', 11, 'bold'))

studenttable = ttk.Treeview(rightframe, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'),
                            xscrollcommand=Scrollbarx.set, yscrollcommand=Scrollbary.set)

Scrollbarx.pack(side=BOTTOM, fill=X)
Scrollbary.pack(side=RIGHT, fill=Y)

studenttable.pack(fill=BOTH, expand=1)
studenttable.config(show='headings')

studenttable.heading('Id', text='Id')
studenttable.heading('Name', text='Name')
studenttable.heading('Mobile', text='Mobile')
studenttable.heading('Email', text='Email')
studenttable.heading('Address', text='Address')
studenttable.heading('Gender', text='Gender')
studenttable.heading('DOB', text='DOB')
studenttable.heading('Added Date', text='Added Date')
studenttable.heading('Added Time', text='Added Time')

studenttable.column('Id', width=50, anchor=CENTER)
studenttable.column('Name', width=150)
studenttable.column('Mobile', width=100, anchor=CENTER)
studenttable.column('Email', width=150)
studenttable.column('Address', width=150)
studenttable.column('Gender', width=80, anchor=CENTER)
studenttable.column('DOB', width=100, anchor=CENTER)
studenttable.column('Added Date', width=100, anchor=CENTER)
studenttable.column('Added Time', width=100, anchor=CENTER)

Scrollbarx.config(command=studenttable.xview)
Scrollbary.config(command=studenttable.yview)

root.mainloop()
