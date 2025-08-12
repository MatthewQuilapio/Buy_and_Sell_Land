import tkinter as tk
import subprocess
import sys
from tkinter import *
from tkinter import ttk
from window_config import window_config
#from tkinter import messagebox                                             
from sql_database import connection
from input_sell import add_to_sell_command
from input_sell import display_sell
from buy_view import display_buy
from search_sql import *

conn = connection()
cursor = conn.cursor()


head_font_style = ("Arial", 16, "bold")
button_font_style = ("Arial", 12, "bold")
sell_products = {'land_address':[], 'seller_name':[]}

current_page = None
def option_menu(root):
    frameoption = tk.Frame(root, bg='red')
    frameoption.pack(side="left", fill="both")
    frameoption.pack_propagate()
    frameoption.configure(width=200, height=650)
    #home_btn = tk.Button(frameoption, font=button_font_style, text="Dashboard", command=header_section, bg="#FF2E97") 
    #home_btn.pack(padx=5, pady=5)
    buy_btn = tk.Button(frameoption, font=button_font_style, text="Buy/Lease", command=lambda:buy_section(root), bg="#FF2E97") 
    buy_btn.pack(padx=5, pady=5)
    sell_btn = tk.Button(frameoption, font=button_font_style, text="Sell", command=lambda:sell_section(root), bg="#FF2E97") 
    sell_btn.pack(padx=5, pady=5)
    #lease_btn = tk.Button(frameoption, font=button_font_style, text="Lease", bg="#FF2E97") 
    #lease_btn.pack(padx=5, pady=5)
    rent_btn = tk.Button(frameoption, font=button_font_style, text="Log Out", command=lambda:logout_func(root), bg="#FF2E97") 
    rent_btn.pack(padx=5, pady=5)

def change_frame(new_frame):
    global current_page
    if current_page is not None:
        current_page.destroy()
    current_page = new_frame
    current_page.pack()

def logout_func(root):
    root.destroy()
    subprocess.run([sys.executable, "login_page.py"])
    

def header_section():
    header_dashboard = tk.Label(root, text="DASHBOARD", bg= 'green', anchor='w', fg = 'white', justify="center", font=head_font_style)
    header_dashboard.pack(side="top", fill="x", padx=5, pady=5, ipadx=5, ipady=5)
    change_frame(header_dashboard)

def buy_section(root):
    buy_frame = tk.Frame(root, width=500, bg="#FF2E97")
    #buy_frame.config(bg="#FF2E97")
    buy_frame.pack(padx=5, pady=5, side="left", fill="both", expand=True)
    #buy_frame.pack(padx=5, pady=5, side="left", fill="both", expand=True)
    buy_label = tk.Label(buy_frame, text="BUY", anchor='w', fg="#5D3A9B", bg="#FF2E97", font=head_font_style) 
    buy_label.pack()
    buy_buttons_frame = tk.Frame(buy_frame)
    buy_buttons_frame.config(bg="#000000")
    buy_buttons_frame.pack()
    #buy_list = tk.Listbox(buy_frame, height=25)
    #buy_list.pack(fill="both", padx=5, pady=5)

    refresh_btn = tk.Button(buy_buttons_frame, font=button_font_style, text="Refresh", command=lambda:display_buy(tree), bg="#FF2E97") 
    refresh_btn.pack(side = "left")

    search_input_buy = tk.Entry(buy_buttons_frame, text="Search")
    search_input_buy.pack(side = "left")
    search_button = tk.Button(buy_buttons_frame,font=button_font_style, text="Go", command=lambda:search_item_buy(search_input_buy, tree))
    search_button.pack(side = "left")
    
    tree = ttk.Treeview(buy_frame, selectmode ='browse')
    tree.pack(side='left',expand=True, fill='both')
    
    display_buy(tree)
    change_frame(buy_frame)

def sell_section(root):
    style = ttk.Style()
    style.configure("custom_sell_frame.TFrame", foreground="red", background="#3EC8FF")

    sell_frame = ttk.Frame(root, width=500, style="custom_sell_frame.TFrame")
    #sell_frame.config(background="#3EC8FF")
    sell_frame.pack(padx=5, pady=5, side="left", fill="both", expand=True)

    sell_label = tk.Label(sell_frame, text="SELL", anchor='w', fg="#483F72", bg="#3EC8FF", font=head_font_style) 
    sell_label.pack()
    
    sell_buttons_frame = tk.Frame(sell_frame)
    sell_buttons_frame.config(bg="#000000")
    sell_buttons_frame.pack()

    add_to_sell = tk.Button(sell_buttons_frame, font=button_font_style, text="Add to Sell (+)", command=lambda: add_to_sell_command(), bg="#FF2E97") 
    add_to_sell.pack(side = "left")
    refresh_btn = tk.Button(sell_buttons_frame, font=button_font_style, text="Refresh", command=lambda: display_sell(sell_frame, tree), bg="#FF2E97") 
    refresh_btn.pack(side = "left")

    search_input_sell = tk.Entry(sell_buttons_frame, text="Search")
    search_input_sell.pack(side = "left")
    search_button = tk.Button(sell_buttons_frame,font=button_font_style, text="Go", command=lambda:search_item_sell(search_input_sell, tree))
    search_button.pack(side = "left")

    tree = ttk.Treeview(sell_frame, selectmode ='browse')
    tree.pack(side='left',expand=True, fill='both')
    """verscrlbar = ttk.Scrollbar(root,  
                           orient ="vertical",  
                           command = tree.yview)
    tree.configure(yscrollcommand = verscrlbar.set)
    verscrlbar.pack(side ='right', fill ='y')"""

    #listbox_header(sell_frame)
    
    #sell_list = tk.Listbox(sell_frame, height=25)
    #sell_list.pack(fill="both", padx=5, pady=5)
         
    display_sell(tree)
    change_frame(sell_frame)  
 
def main_function():
    root = tk.Tk()
    root.title("Land Buy and Sell")

    x,y = window_config(1000, 650, root)

    root.geometry(f'{1000}x{650}+{x}+{y}')
    root.configure(bg = 'indigo')
    root.resizable(False, False)
    #buy_section()
    #sell_section()
    option_menu(root)
    #header_section()
    buy_section(root) 
    root.mainloop()
    conn.close()
#main_function()