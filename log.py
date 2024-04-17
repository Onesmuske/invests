import os
import re
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')
window.resizable(0, 0)
window.title('Login and Registration Page')

# Window Icon Photo
icon = PhotoImage(file='images\\pic-icon.png')
window.iconphoto(True, icon)

LoginPage = Frame(window)
RegistrationPage = Frame(window)

for frame in (LoginPage, RegistrationPage):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()


show_frame(LoginPage)


# ========== DATABASE VARIABLES ============
Email = StringVar()
FullName = StringVar()
Password = StringVar()
ConfirmPassword = StringVar()


# ==================== LOGIN PAGE ======================
design_frame1 = Listbox(LoginPage, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame1.place(x=0, y=0)

design_frame2 = Listbox(LoginPage, bg='#1e85d0', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame2.place(x=676, y=0)

design_frame3 = Listbox(LoginPage, bg='#1e85d0', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame3.place(x=75, y=106)

design_frame4 = Listbox(LoginPage, bg='#f8f8f8', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame4.place(x=676, y=106)

# ====== Email ====================
email_entry = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                    textvariable=Email)
email_entry.place(x=134, y=170, width=256, height=34)
email_entry.config(highlightbackground="black", highlightcolor="black")
email_label = Label(design_frame4, text='• Email account', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
email_label.place(x=130, y=140)

# ==== Password ==================
password_entry1 = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                        textvariable=Password)
password_entry1.place(x=134, y=250, width=256, height=34)
password_entry1.config(highlightbackground="black", highlightcolor="black")
password_label = Label(design_frame4, text='• Password', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
password_label.place(x=130, y=220)

# function for show and hide password
def password_command():
    if password_entry1.cget('show') == '•':
        password_entry1.config(show='')
    else:
        password_entry1.config(show='•')


# ====== checkbutton ==============
checkButton = Checkbutton(design_frame4, bg='#f8f8f8', command=password_command, text='Show Password')
checkButton.place(x=140, y=288)

# ========= Buttons ===============
SignUp_button = Button(LoginPage, text='Sign up', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                       command=lambda: show_frame(RegistrationPage), borderwidth=0, activebackground='#1b87d2', cursor='hand2')
SignUp_button.place(x=1100, y=175)

# ===== Welcome Label ==============
welcome_label = Label(design_frame4, text='Welcome', font=('Arial', 20, 'bold'), bg='#f8f8f8')
welcome_label.place(x=130, y=15)

# ======= top Login Button =========
login_button = Button(LoginPage, text='Login', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                      borderwidth=0, activebackground='#1b87d2', cursor='hand2')
login_button.place(x=845, y=175)

login_line = Canvas(LoginPage, width=60, height=5, bg='#1b87d2')
login_line.place(x=840, y=203)

# ==== LOGIN  down button ============
loginBtn1 = Button(design_frame4, fg='#f8f8f8', text='Login', bg='#1b87d2', font=("yu gothic ui bold", 15),
                   cursor='hand2', activebackground='#1b87d2', command=lambda: login())
loginBtn1.place(x=133, y=340, width=256, height=50)


# ======= ICONS =================

# ===== Email icon =========
email_icon = Image.open('images\\email-icon.png')
photo = ImageTk.PhotoImage(email_icon)
emailIcon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
emailIcon_label.image = photo
emailIcon_label.place(x=105, y=174)

# ===== password icon =========
password_icon = Image.open('images\\pass-icon.png')
photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
password_icon_label.image = photo
password_icon_label.place(x=105, y=254)

# ===== picture icon =========
picture_icon = Image.open('images\\pic-icon.png')
photo = ImageTk.PhotoImage(picture_icon)
picture_icon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
picture_icon_label.image = photo
picture_icon_label.place(x=280, y=5)

# ===== Left Side Picture ============
side_image = Image.open('images\\vector.png')
photo = ImageTk.PhotoImage(side_image)
side_image_label = Label(design_frame3, image=photo, bg='#1e85d0')
side_image_label.image = photo
side_image_label.place(x=50, y=10)


# ============ LOGIN DATABASE CONNECTION =========
connection = sqlite3.connect('RegLog.db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS RegLog(Email TEXT PRIMARY KEY, FullName TEXT, Password TEXT, "
            "ConfirmPassword TEXT)")
connection.commit()
connection.close()


def login():
    conn = sqlite3.connect("RegLog.db")
    cursor = conn.cursor()

    find_user = 'SELECT * FROM RegLog WHERE Email = ? and Password = ?'
    cursor.execute(find_user, [(email_entry.get()), (password_entry1.get())])

    result = cursor.fetchall()
    if result:
        messagebox.showinfo("Success", 'Logged in Successfully.')

        window.destroy()

        os.system('Python loop.py')

    else:
        messagebox.showerror("Failed", "Wrong Login details, please try again.")


# === FORGOT PASSWORD  PAGE ==================================

def forgot_password():
    def change_password():
        if not (email.get() and password.get() and confirmPassword.get()):
            messagebox.showerror("Error", "All fields are required!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email.get()):
            messagebox.showerror("Error", "Invalid email address!")
        elif len(password.get()) < 8:
            messagebox.showerror("Error", "Password should be at least 8 characters long!")
        elif password.get() != confirmPassword.get():
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            db = sqlite3.connect("RegLog.db")
            curs = db.cursor()

            insert = '''update RegLog set Password=?, ConfirmPassword=? where Email=? '''
            curs.execute(insert, [password.get(), confirmPassword.get(), email.get()])
            db.commit()
            db.close()
            messagebox.showinfo('Congrats', 'Password changed successfully')

            os.system('python Main.py')

    win = Toplevel()
    window_width = 350
    window_height = 350
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    win.title('Forgot Password')
    win.iconbitmap('images\\aa.ico')
    win.configure(background='#f8f8f8')
    win.resizable(0, 0)

    # Variables
    email = StringVar()
    password = StringVar()
    confirmPassword = StringVar()

    # ====== Email ====================
    email_entry2 = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                         textvariable=email)
    email_entry2.place(x=40, y=30, width=256, height=34)
    email_entry2.config(highlightbackground="black", highlightcolor="black")
    email_label2 = Label(win, text='• Email account', fg="#89898b", bg='#f8f8f8',
                         font=("yu gothic ui", 11, 'bold'))
    email_label2.place(x=40, y=0)

    # ====  New Password ==================
    new_password_entry = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                               textvariable=password)
    new_password_entry.place(x=40, y=110, width=256, height=34)
    new_password_entry.config(highlightbackground="black", highlightcolor="black")
    new_password_label = Label(win, text='• New Password', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
    new_password_label.place(x=40, y=80)

    # ====  Confirm Password ==================
    confirm_password_entry = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2
                                   , textvariable=confirmPassword)
    confirm_password_entry.place(x=40, y=190, width=256, height=34)
    confirm_password_entry.config(highlightbackground="black", highlightcolor="black")
    confirm_password_label = Label(win, text='• Confirm Password', fg="#89898b", bg='#f8f8f8',
                                   font=("yu gothic ui", 11, 'bold'))
    confirm_password_label.place(x=40, y=160)

    # ======= Update password Button ============
    update_pass = Button(win, fg='#f8f8f8', text='Update Password', bg='#1b87d2', font=("yu gothic ui bold", 14),
                         cursor='hand2', activebackground='#1b87d2', command=change_password)
    update_pass.place(x=40, y=240, width=256, height=50)


forgotPassword = Button(design_frame4, text='Forgot password', font=("yu gothic ui", 8, "bold underline"), bg='#f8f8f8',
                        borderwidth=0, activebackground='#f8f8f8', command=lambda: forgot_password(), cursor="hand2")
forgotPassword.place(x=290, y=290)


# ==================== REGISTRATION PAGE ==============

design_frame5 = Listbox(RegistrationPage, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame5.place(x=0, y=0)

design_frame6 = Listbox(RegistrationPage, bg='#1e85d0', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame6.place(x=676, y=0)

design_frame7 = Listbox(RegistrationPage, bg='#1e85d0', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame7.place(x=75, y=106)

design_frame8 = Listbox(RegistrationPage, bg='#f8f8f8', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame8.place(x=676, y=106)

# ==== Full Name =======
def validate_name(text):
    for char in text:
        if not (char.isalpha() or char.isspace()):
            messagebox.showerror(title='datatype error', message='Invalid input')
            return False
    return True

name_entry = Entry(design_frame8, validate="key", fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                   textvariable=FullName)
name_entry['validatecommand'] = (name_entry.register(validate_name), '%S')
name_entry.place(x=284, y=150, width=286, height=34)
name_entry.config(highlightbackground="black", highlightcolor="black")
name_label = Label(design_frame8, text='•Full Name', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
name_label.place(x=280, y=120)

# ======= Email ===========
email_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                    textvariable=Email)
email_entry.place(x=284, y=220, width=286, height=34)
email_entry.config(highlightbackground="black", highlightcolor="black")
email_label = Label(design_frame8, text='•Email', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
email_label.place(x=280, y=190)

# ====== Password =========
password_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                       textvariable=Password)
password_entry.place(x=284, y=295, width=286, height=34)
password_entry.config(highlightbackground="black", highlightcolor="black")
password_label = Label(design_frame8, text='• Password', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
password_label.place(x=280, y=265)

# ====== Confirm Password ========
confirm_password_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•',
                               highlightthickness=2, textvariable=ConfirmPassword)
confirm_password_entry.place(x=284, y=365, width=286, height=34)
confirm_password_entry.config(highlightbackground="black", highlightcolor="black")
confirm_password_label = Label(design_frame8, text='• Confirm Password', fg="#89898b", bg='#f8f8f8',
                               font=("yu gothic ui", 11, 'bold'))
confirm_password_label.place(x=280, y=335)

# ========= Show Password Button ==========
def show_password():
    if password_entry.cget('show') == '•':
        password_entry.config(show='')
    else:
        password_entry.config(show='•')

    if confirm_password_entry.cget('show') == '•':
        confirm_password_entry.config(show='')
    else:
        confirm_password_entry.config(show='•')

# ========= Show Password Button ==========
showPasswordButton = Checkbutton(design_frame8, bg='#f8f8f8', command=show_password, text='Show Password')
showPasswordButton.place(x=150, y=415)

# ========= Register function ==========
def register():
    if not (FullName.get() and Email.get() and Password.get() and ConfirmPassword.get()):
        messagebox.showerror("Error", "All fields are required!")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", Email.get()):
        messagebox.showerror("Error", "Invalid email address!")
    elif len(Password.get()) < 8:
        messagebox.showerror("Error", "Password should be at least 8 characters long!")
    elif Password.get() != ConfirmPassword.get():
        messagebox.showerror("Error", "Passwords do not match!")
    else:
        connection = sqlite3.connect('RegLog.db')
        cur = connection.cursor()
        cur.execute("INSERT INTO RegLog VALUES (?, ?, ?, ?)", (Email.get(), FullName.get(), Password.get(), ConfirmPassword.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Registration successful!")
        show_frame(LoginPage)
        # Clearing the registration fields after registration
        FullName.set('')
        Email.set('')
        Password.set('')
        ConfirmPassword.set('')


# ========= Register Button =========
register_button = Button(RegistrationPage, text='Register', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                         borderwidth=0, activebackground='#1b87d2', cursor='hand2', command=register)
register_button.place(x=1100, y=520)

# ========== back Button ==========
back_button = Button(RegistrationPage, text='Back', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                     borderwidth=0, activebackground='#1b87d2', cursor='hand2', command=lambda: show_frame(LoginPage))
back_button.place(x=845, y=240)

# ========= Main Function ===========
window.mainloop()
