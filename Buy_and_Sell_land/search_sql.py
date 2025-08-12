from tkinter import *
from window_config import window_config
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
    #search_list1.delete(0,END)
    cursor.execute(search_sell_query, ('%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%',))
    results = cursor.fetchall()
    search_list1 = listbox_header(results, sell_tree)
    
    """ctr = 0
    for x in results:
        search_list1.insert(END, x)
        ctr+=1"""
    search_list1.bind('<Double-1>', view_sell_details)

def search_item_buy(search_word, buy_tree):
    #search_list2.delete(0,END)
    cursor.execute(search_buy_query, ('%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%', '%'+search_word.get()+'%',))
    results = cursor.fetchall()
    search_list2 = listbox_header(results, buy_tree)
    """ctr = 0
    for x in results:
        search_list2.insert(END, x)
        ctr+=1"""
    search_list2.bind('<Double-1>', view_buy_details)