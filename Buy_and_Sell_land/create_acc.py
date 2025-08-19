"""
    Module: create_account.py
    Description: Tkinter GUI module for creating new user 
                 accounts and storing them in the database.
    Author: Angelo Matthew Quilapio
    License: All Rights Reserved
"""
import tkinter as tk
import subprocess
import sys
from tkinter import messagebox
from window_config import window_config
from sql_database import connection


create_table_acc = """
CREATE TABLE IF NOT EXISTS lands_acc_list (
    acc_id int NOT NULL AUTO_INCREMENT,
    surname_var VARCHAR(255) NOT NULL,
    firstname_var VARCHAR(255) NOT NULL,
    username_var VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20),
    email_info VARCHAR(100) NOT NULL,
    password_var VARCHAR(255) NOT NULL,
    PRIMARY KEY (acc_id)
);
"""

conn = connection()
cursor = conn.cursor()


cursor.execute(create_table_acc)



def fill_up_acc(login_page):
    """
    Launch the Tkinter account creation window, allowing users 
    to input personal and login credentials.

    Parameters:
        login_page (tk.Tk): Current login window instance 
                            to be destroyed before launching 
                            the account creation page.
    """

    # Destroy the login window and open new account creation page
    login_page.destroy()
    createacc_page = tk.Tk()
    createacc_page.title("Create Account")
    button_font_style = ("Arial", 12, "bold")

    # Configure window size and position
    x,y = window_config(500, 550, createacc_page)
    createacc_page.geometry(f'{500}x{550}+{x}+{y}')
    createacc_page.configure(bg = 'indigo')
    createacc_page.resizable(False, False)    
    
    # Main container frame
    fillup_frame = tk.Frame(createacc_page, width=500, background="#5D3A9B")
    fillup_frame.pack(padx=5, pady=5, side="top", fill="both", expand=True)

    # Form fields for account information
    tk.Label(fillup_frame, text="Last Name:").pack(anchor="w", pady=(0,2)) 
    surname_entry = tk.Entry(fillup_frame)
    surname_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

    tk.Label(fillup_frame, text="First Name:").pack(anchor="w", pady=(0,2)) 
    firstname_entry = tk.Entry(fillup_frame)
    firstname_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

    tk.Label(fillup_frame, text="User Name:").pack(anchor="w", pady=(0,2)) 
    username_entry = tk.Entry(fillup_frame)
    username_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

    tk.Label(fillup_frame, text="Contact No:").pack(anchor="w", pady=(0,2)) 
    contact_entry = tk.Entry(fillup_frame)
    contact_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

    tk.Label(fillup_frame, text="Email Address:").pack(anchor="w", pady=(0,2)) 
    email_entry = tk.Entry(fillup_frame)
    email_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

    tk.Label(fillup_frame, text="Password:").pack(anchor="w", pady=(0,2)) 
    password_entry = tk.Entry(fillup_frame, show='*')
    password_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

    tk.Label(fillup_frame, text="Re-enter Password:").pack(anchor="w", pady=(0,2)) 
    repassword_entry = tk.Entry(fillup_frame, show='*')
    repassword_entry.pack(fill="x", pady=(10, 10), padx=(10, 10))

    tk.Button(fillup_frame, font=button_font_style, text="Confirm", command=lambda: update_acc_table(surname_entry,
    firstname_entry, username_entry, contact_entry, email_entry, password_entry, repassword_entry, createacc_page)).pack()

    createacc_page.mainloop()



def update_acc_table(entry1, entry2, entry3, entry4, entry5, entrypass, entryrepass, createacc_page):
    """
    Validate input fields and insert account details into 
    the database if all checks pass.

    Parameters:
        entry1, entry2, entry3, entry4, entry5 (tk.Entry): 
            Tkinter Entry widgets for surname, firstname, 
            username, contact number, and email.
        entrypass, entryrepass (tk.Entry): 
            Tkinter Entry widgets for password and confirm password.
        createacc_page (tk.Tk): Account creation page instance 
                                to be closed upon successful insertion.
    """

    # Validate contact number (must be 11 digits)
    if entry4.get().isdigit() and (len(entry4.get()) == 11):
        # Validate email format (basic Gmail check)
        if '@gmail.com' in entry5.get():
        # Validate password strength and match
            if (len(entrypass.get()) < 8) or (len(entryrepass.get()) < 8) :
                messagebox.showerror("Error Message", "Missing input")
            elif (entrypass.get() != entryrepass.get()):
                messagebox.showerror("Error Message", "Password don't match.")
            elif (entrypass.get() == entryrepass.get()):
                # Prepare SQL insert statement
                for_insert = (entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entrypass.get())
                insert_acc_sql = """INSERT INTO lands_acc_list (surname_var, firstname_var, username_var, 
                contact_number, email_info, password_var)
                    VALUES (%s, %s, %s, %s, %s, %s);"""
                cursor.execute(insert_acc_sql, for_insert)
                result = cursor.rowcount

                # Commit transaction if successful
                if result > 0:
                    conn.commit()
                    createacc_page.destroy()
                    subprocess.run([sys.executable, "login_page.py"])
                else:
                    messagebox.showerror("Error Message", "Missing input")
        else:
            messagebox.showerror("Error Message", "Invalid Email")
    else:
        messagebox.showerror("Error Message", "Contact No input error")
    