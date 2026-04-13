from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required')
    elif usernameEntry.get() == 'admin' and passwordEntry.get() == 'admin':
        messagebox.showinfo('Success', 'Login successful')
        window.destroy()
        import sms


window = Tk()

window.geometry('1200x700+0+0')
window.resizable(False, False)
window.title('Student Management System - Login')

backgroundImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)

loginframe = Frame(window, bg='white', bd=10, relief=GROOVE)
loginframe.place(x=400, y=150, width=400, height=450)

logoImage = PhotoImage(file='std.png')
logoLabel = Label(loginframe, image=logoImage, bg='white')
logoLabel.grid(row=0, column=0, pady=20, padx=20)

usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginframe, image=usernameImage, text=' Username', compound=LEFT, font=(
    'times new roman', 18, 'bold'), bg='white', fg='#2c3e50')
usernameLabel.grid(row=1, column=0, pady=10, padx=20, sticky=W)

usernameEntry = Entry(loginframe, font=(
    'times new roman', 18, 'bold'), bd=3, relief=GROOVE, width=25)
usernameEntry.grid(row=2, column=0, pady=5, padx=20)

passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginframe, image=passwordImage, text=' Password', compound=LEFT, font=(
    'times new roman', 18, 'bold'), bg='white', fg='#2c3e50')
passwordLabel.grid(row=3, column=0, pady=10, padx=20, sticky=W)

passwordEntry = Entry(loginframe, font=(
    'times new roman', 18, 'bold'), bd=3, relief=GROOVE, show='*', width=25)
passwordEntry.grid(row=4, column=0, pady=5, padx=20)

LoginButtun = Button(loginframe, text='Login', width=15, font=(
    'times new roman', 14, 'bold'), bg='#3498db', fg='white', command=login, cursor='hand2', bd=0, pady=5)
LoginButtun.grid(row=5, column=0, pady=30)

window.mainloop()
