"""
Search SQL Module (Tkinter GUI)

This module provides functions to search land listings (buy/sell) 
from the database and display them in a Tkinter Treeview.

Modules:
    - tkinter: For GUI components
    - sql_database: Database connection
    - input_sell: Functions for viewing sell details
    - buy_view: Functions for viewing buy details
    - listbox: Helper for creating Treeview headers

Author: Angelo Matthew Quilapio
License: All Rights Reserved
"""

from tkinter import *
from sql_database import connection
from input_sell import view_sell_details
from buy_view import view_buy_details
from listbox import *

conn = connection()
cursor = conn.cursor()

search_sell_query = f"""
    SELECT land_id, seller_name, land_price,
    province_name, contact_number FROM lands_for_selling
    WHERE land_id LIKE %s OR
    seller_name LIKE %s OR
    land_price LIKE %s OR 
    province_name LIKE %s OR
    contact_number LIKE %s;
"""

search_buy_query = f"""
    SELECT land_id, seller_name, land_price,
    province_name, contact_number FROM lands_for_selling
    WHERE land_id LIKE %s OR
    seller_name LIKE %s OR
    land_price LIKE %s OR 
    province_name LIKE %s OR
    contact_number LIKE %s;
"""

def search_item_sell(search_word, sell_tree):
    """
    Search for land in the 'Sell' section.

    Args:
        search_word (tk.Entry): Entry widget containing the search keyword
        sell_tree (ttk.Treeview): Treeview widget to display results
    """

    # Execute SQL query with wildcard matching
    cursor.execute(search_sell_query, ('%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%',))
    results = cursor.fetchall()

    # Display results in Treeview
    search_list1 = listbox_header(results, sell_tree)
    
    # Bind double-click event to view details
    search_list1.bind('<Double-1>', view_sell_details)

def search_item_buy(search_word, buy_tree):
    """
    Search for land in the 'Buy' section.

    Args:
        search_word (tk.Entry): Entry widget containing the search keyword
        buy_tree (ttk.Treeview): Treeview widget to display results
    """

    cursor.execute(search_buy_query, ('%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%',))
    results = cursor.fetchall()

    search_list2 = listbox_header(results, buy_tree)

    search_list2.bind('<Double-1>', view_buy_details)