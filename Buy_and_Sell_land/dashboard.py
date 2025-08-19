"""
Land Buy & Sell Application (Tkinter GUI)

This module provides a GUI for buying, selling, and searching land listings.
It connects to an SQL database, allows users to switch between Buy and Sell
sections, and includes a logout function to return to the login page.

Modules:
    - tkinter: For GUI components
    - subprocess, sys: For restarting the application with login page
    - window_config: Custom window positioning
    - sql_database: Database connection
    - input_sell: Functions for adding/displaying sell listings
    - buy_view: Functions for displaying buy listings
    - search_sql: Functions for searching listings

Author: Angelo Matthew Quilapio
License: All Rights Reserved
"""

import tkinter as tk
import subprocess
import sys
from tkinter import *
from tkinter import ttk
from window_config import window_config                                            
from sql_database import connection
from input_sell import add_to_sell_command
from input_sell import display_sell
from buy_view import display_buy
from search_sql import *

# Establish database connection
conn = connection()
cursor = conn.cursor()


head_font_style = ("Arial", 16, "bold")
button_font_style = ("Arial", 12, "bold")

# Tracks the currently active page/frame
current_page = None


def option_menu(root, list_acc):
    """
    Create the left-side navigation menu.

    Args:
        root (tk.Tk): Main application window
        list_acc (list): Logged-in account details
    """
    frameoption = tk.Frame(root, bg='red')
    frameoption.pack(side="left", fill="both")
    frameoption.pack_propagate()
    frameoption.configure(width=200, height=650)

    buy_btn = tk.Button(frameoption, font=button_font_style, text="Buy/Lease", command=lambda:buy_section(root, list_acc), bg="#FF2E97") 
    buy_btn.pack(padx=5, pady=5)
    sell_btn = tk.Button(frameoption, font=button_font_style, text="Sell", command=lambda:sell_section(root, list_acc), bg="#FF2E97") 
    sell_btn.pack(padx=5, pady=5)

    rent_btn = tk.Button(frameoption, font=button_font_style, text="Log Out", command=lambda:logout_func(root), bg="#FF2E97") 
    rent_btn.pack(padx=5, pady=5)

def change_frame(new_frame):
    """
    Replace the currently displayed frame with a new one.

    Args:
        new_frame (tk.Frame): The frame to display
    """
    global current_page
    if current_page is not None:
        current_page.destroy()
    current_page = new_frame
    current_page.pack()

def logout_func(root):
    """
    Log out by closing the current window and reopening the login page.

    Args:
        root (tk.Tk): Main application window
    """
    root.destroy()
    subprocess.run([sys.executable, "login_page.py"])


def buy_section(root, list_acc):
    """
    Display the Buy/Lease section.

    Args:
        root (tk.Tk): Main application window
        list_acc (list): Logged-in account details
    """

    # Control panel
    buy_frame = tk.Frame(root, width=500, bg="#FF2E97")
    buy_frame.pack(padx=5, pady=5, side="left", fill="both", expand=True)

    buy_label = tk.Label(buy_frame, text="BUY", anchor='w', fg="#5D3A9B", bg="#FF2E97", font=head_font_style) 
    buy_label.pack()
    buy_buttons_frame = tk.Frame(buy_frame)
    buy_buttons_frame.config(bg="#000000")
    buy_buttons_frame.pack()

    refresh_btn = tk.Button(buy_buttons_frame, font=button_font_style, text="Refresh", command=lambda:display_buy(tree, list_acc), bg="#FF2E97") 
    refresh_btn.pack(side = "left")

    search_input_buy = tk.Entry(buy_buttons_frame, text="Search")
    search_input_buy.pack(side = "left")
    search_button = tk.Button(buy_buttons_frame,font=button_font_style, text="Go", command=lambda:search_item_buy(search_input_buy, tree))
    search_button.pack(side = "left")
    
    # Table view
    tree = ttk.Treeview(buy_frame, selectmode ='browse')
    tree.pack(side='left',expand=True, fill='both')
    
    # Load initial data
    display_buy(tree, list_acc)
    change_frame(buy_frame)

def sell_section(root, list_acc):
    """
    Display the Sell section.

    Args:
        root (tk.Tk): Main application window
        list_acc (list): Logged-in account details
    """
    style = ttk.Style()
    style.configure("custom_sell_frame.TFrame", foreground="red", background="#3EC8FF")

    # Control panel
    sell_frame = ttk.Frame(root, width=500, style="custom_sell_frame.TFrame")
    sell_frame.pack(padx=5, pady=5, side="left", fill="both", expand=True)

    sell_label = tk.Label(sell_frame, text="SELL", anchor='w', fg="#483F72", bg="#3EC8FF", font=head_font_style) 
    sell_label.pack()
    
    sell_buttons_frame = tk.Frame(sell_frame)
    sell_buttons_frame.config(bg="#000000")
    sell_buttons_frame.pack()

    
    add_to_sell = tk.Button(sell_buttons_frame, font=button_font_style, text="Add to Sell (+)", command=lambda: add_to_sell_command(list_acc), bg="#FF2E97") 
    add_to_sell.pack(side = "left")
    refresh_btn = tk.Button(sell_buttons_frame, font=button_font_style, text="Refresh", command=lambda: display_sell(tree, list_acc), bg="#FF2E97") 
    refresh_btn.pack(side = "left")

    search_input_sell = tk.Entry(sell_buttons_frame, text="Search")
    search_input_sell.pack(side = "left")
    search_button = tk.Button(sell_buttons_frame,font=button_font_style, text="Go", command=lambda:search_item_sell(search_input_sell, tree))
    search_button.pack(side = "left")

    # Table view
    tree = ttk.Treeview(sell_frame, selectmode ='browse')
    tree.pack(side='left',expand=True, fill='both')

    # Load initial data   
    display_sell(tree, list_acc)
    change_frame(sell_frame)  
 
def main_function(list_acc):
    """
    Launch the Land Buy & Sell application.

    Args:
        list_acc (list): Logged-in account details
    """
    root = tk.Tk()
    root.title("Land Buy and Sell")

    # Configure window size and position
    x,y = window_config(1000, 650, root)
    root.geometry(f'{1000}x{650}+{x}+{y}')
    root.configure(bg = 'indigo')
    root.resizable(False, False)

    # Build menu and default section
    option_menu(root, list_acc)
    buy_section(root, list_acc) 
    root.mainloop()

    # Close DB connection
    conn.close()