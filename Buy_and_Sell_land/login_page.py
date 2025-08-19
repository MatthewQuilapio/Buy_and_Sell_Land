"""
Login Page for Land Buy & Sell Application

This script launches a Tkinter-based login window that authenticates
users from an SQL database. On successful login, it opens the main
dashboard. Users can also create a new account.

Modules:
    tkinter          - For GUI components
    window_config    - For window positioning
    sql_database     - For database connection
    dashboard        - For launching main application after login
    create_acc       - For creating new user accounts

Author: Angelo Matthew Quilapio
License: All Rights Reserved
"""

import tkinter as tk
from window_config import window_config
from sql_database import connection
from dashboard import main_function
from create_acc import fill_up_acc


conn = connection()
cursor = conn.cursor()

login_page = tk.Tk()
login_page.title("Login")
button_font_style = ("Arial", 12, "bold")

# Set window position and size
x,y = window_config(300, 250, login_page)
login_page.geometry(f'{300}x{250}+{x}+{y}')
login_page.configure(bg = 'indigo')
login_page.resizable(False, False)

# SQL query for user authentication
select_table_acc = f"""
SELECT * from lands_acc_list where username_var = %s and password_var = %s;
"""

# Establish database connection
conn = connection()
cursor = conn.cursor()

def confirm_acc(user_entry, pass_entry):
    """
    Validate login credentials and launch main dashboard.

    Args:
        user_entry (tk.Entry): Entry widget for username
        pass_entry (tk.Entry): Entry widget for password
    """

    # Get credentials from input fields
    for_login = (user_entry.get(), pass_entry.get())

    # Query database
    cursor.execute(select_table_acc, for_login)
    acc_result = cursor.fetchall()

    # Flatten fetched data into a single list
    list_acc = [item for temp in acc_result for item in temp]

    # Check if entered credentials match
    if (user_entry.get() in list_acc) and (pass_entry.get() in list_acc):
        login_page.destroy()
        main_function(list_acc)
        
# ------------------------- LAYOUT -------------------------
# Frame for username & password fields
fillup_frame = tk.Frame(login_page, width=500, background="#5D3A9B")
fillup_frame.pack(padx=5, pady=5, side="top", fill="both", expand=True)

# Frame for action buttons
button_frame = tk.Frame(login_page, width=500, background="#5D3A9B")
button_frame.pack(padx=5, pady=5, side="top", fill="both", expand=True)

# Username field
tk.Label(fillup_frame, text="UserName:").pack(anchor="w", pady=(0,2)) 
username_entry = tk.Entry(fillup_frame)
username_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

# Password Field
tk.Label(fillup_frame, text="Password:").pack(anchor="w", pady=(0,2)) 
password_entry = tk.Entry(fillup_frame, show='*')
password_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))                             

# Log In button
tk.Button(button_frame, font=button_font_style, text="Log In", command = lambda:confirm_acc(username_entry, password_entry)).pack(side='left')

#Create Account button
tk.Button(button_frame, font=button_font_style, text="Create New Account", command= lambda:fill_up_acc(login_page)).pack(side='left')



login_page.mainloop()