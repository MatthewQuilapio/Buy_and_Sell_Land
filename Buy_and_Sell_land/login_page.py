import tkinter as tk
from window_config import window_config
from tkinter import messagebox
from sql_database import connection
from dashboard import main_function
from create_acc import fill_up_acc


conn = connection()
cursor = conn.cursor()

login_page = tk.Tk()
login_page.title("Login")
button_font_style = ("Arial", 12, "bold")

x,y = window_config(300, 250, login_page)
login_page.geometry(f'{300}x{250}+{x}+{y}')
login_page.configure(bg = 'indigo')
login_page.resizable(False, False)

"""def hide_pass():
    password_entry.config(show='*')
    checkbutton.config(command=show_pass)
def show_pass():
    password_entry.config(show='')
    checkbutton.config(command=hide_pass)"""
select_table_acc = f"""
SELECT acc_id, username_var, password_var from lands_acc_list where username_var = %s and password_var = %s;
"""

conn = connection()
cursor = conn.cursor()

def confirm_acc(user_entry, pass_entry):
    for_login = (user_entry.get(), pass_entry.get())
    cursor.execute(select_table_acc, for_login)
    acc_result = cursor.fetchall()
    name_result = [i[1] for i in acc_result]
    pass_result = [i[2] for i in acc_result]
    id_result = [i[0] for i in acc_result]
    print(id_result)
    #conn.commit()
    if (user_entry.get() in name_result) and (pass_entry.get() in pass_result):
        login_page.destroy()
        main_function()
        
        
        #messagebox.showinfo("Login", "You're in")

fillup_frame = tk.Frame(login_page, width=500, background="#5D3A9B")
fillup_frame.pack(padx=5, pady=5, side="top", fill="both", expand=True)
button_frame = tk.Frame(login_page, width=500, background="#5D3A9B")
button_frame.pack(padx=5, pady=5, side="top", fill="both", expand=True)

tk.Label(fillup_frame, text="UserName:").pack(anchor="w", pady=(0,2)) 
username_entry = tk.Entry(fillup_frame)
username_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

tk.Label(fillup_frame, text="Password:").pack(anchor="w", pady=(0,2)) 
password_entry = tk.Entry(fillup_frame, show='*')
password_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

#checkbutton = tk.Checkbutton(login_page, text="Show Password", command=show_pass,onvalue=1, offvalue=0).pack()
                             

tk.Button(button_frame, font=button_font_style, text="Confirm", command = lambda:confirm_acc(username_entry, password_entry)).pack(side='left')
tk.Button(button_frame, font=button_font_style, text="Create New Account", command= lambda:fill_up_acc(login_page)).pack(side='left')



login_page.mainloop()