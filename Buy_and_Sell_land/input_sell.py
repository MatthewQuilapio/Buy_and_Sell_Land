import mysql.connector
import tkinter as tk
import string
import random
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from window_config import window_config
from sql_database import connection
from view_map import *
from listbox import listbox_header




button_font_style = ("Arial", 12, "bold")
yes_no = ("Yes", "No")
conn = connection()
cursor = conn.cursor()
display_basic_info=f"""select land_id, seller_name, land_price, province_name, contact_number from lands_for_selling where acc_id = %s;"""
create_table_sql = """
CREATE TABLE IF NOT EXISTS lands_for_selling (
    land_id VARCHAR(100) PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    land_price VARCHAR(100) NOT NULL, 
    st_add VARCHAR(255) NOT NULL,
    province_name VARCHAR(255) NOT NULL,
    city_name VARCHAR(255) NOT NULL,
    post_no VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20),
    email_info VARCHAR(100) NOT NULL,
    size_sq_meters VARCHAR(255) NOT NULL,
    title VARCHAR(150) NOT NULL,                 
    status VARCHAR(150) NOT NULL,
    acc_id VARCHAR(150) NOT NULL,
    listed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

cursor.execute(create_table_sql)

def generate_id_value(gen_value, id_list):
    while(1):
        if not gen_value in id_list:
            return gen_value
        else:
            gen_value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    

def add_to_sell_command(list_acc):
    window = tk.Tk()
    window.title("What you want to sell?")
    window.resizable(False, False)
    x,y = window_config(750, 550, window)
    window.geometry(f'{750}x{550}+{x}+{y}')

    cursor.execute('SELECT prov_name FROM province_list ORDER BY prov_name')
    province_result = cursor.fetchall()
    #print(province_result[0])
    province_list = [i[0] for i in province_result]

    #to view current id lists
    cursor.execute('SELECT land_id FROM lands_for_selling')
    land_id_result = cursor.fetchall()
    land_id_result = [i[0] for i in land_id_result]

    #for seller name
    seller_name  = list_acc[2] + ' ' + list_acc[1]
    #print(seller_name)

    id_value_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    id_value = generate_id_value(id_value_str, land_id_result)

    fillout_frame = tk.Frame(window, padx=18, pady=16) 
    fillout_frame.pack(side="left",fill="both", expand=True)

    fillout_frame_2 = tk.Frame(window, padx=18, pady=16) 
    fillout_frame_2.pack(side="left",fill="both", expand=True)

    tk.Label(fillout_frame, text="ID:").pack(anchor="w", pady=(0,2)) 
    id_entry = tk.Label(fillout_frame, text=id_value)
    id_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Seller Name:").pack(anchor="w", pady=(0,2)) 
    name_entry = tk.Label(fillout_frame, text=seller_name)
    name_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Selling Price:").pack(anchor="w", pady=(0,2)) 
    price_entry = tk.Entry(fillout_frame)
    price_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame_2, text="Street Address:").pack(anchor="w", pady=(0,2)) 
    address_entry = tk.Entry(fillout_frame_2)
    address_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame_2, text="Province:").pack(anchor="w", pady=(0,2)) 
    province_entry = ttk.Combobox(fillout_frame_2, values=province_list)
    province_entry.pack(fill="x", pady=(0, 10))
    #province_entry.set("CITY OF MANILA")
    tk.Label(fillout_frame_2, text="City:").pack(anchor="w", pady=(0,2)) 
    city_entry = ttk.Combobox(fillout_frame_2)
    city_entry.pack(fill="x", pady=(0, 10))

    province_entry.bind("<<ComboboxSelected>>", lambda event: update_city_entry(event, city_entry))

    tk.Label(fillout_frame_2, text="ZIP:").pack(anchor="w", pady=(0,2)) 
    zip_entry = tk.Entry(fillout_frame_2)
    zip_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Seller Contact Info:").pack(anchor="w", pady=(0,2)) 
    contact_entry = tk.Label(fillout_frame, text=list_acc[4])
    contact_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Seller Email Info:").pack(anchor="w", pady=(0,2))
    email_entry = tk.Label(fillout_frame, text=list_acc[5])
    email_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Square Meter:").pack(anchor="w", pady=(0,2))
    area_entry = tk.Entry(fillout_frame)
    area_entry.pack(fill="x", pady=(0, 10))

    avail_not = ["Available", "Sold"]
    #opt = StringVar(value="Available")  
    tk.Label(fillout_frame, text="Status:").pack(anchor="w", pady=(0,2))
    status_entry = ttk.Combobox(fillout_frame, values=avail_not)
    status_entry.pack(fill="x", pady=(0, 10)) 

    yes_no = ["Yes", "No"]
    tk.Label(fillout_frame, text="Title:").pack(anchor="w", pady=(0,2))
    title_entry = ttk.Combobox(fillout_frame, values=yes_no)
    title_entry.pack(fill="x", pady=(0, 10))  

    tk.Button(fillout_frame, font=button_font_style, text="Confirm", command=lambda: 
              add_to_sell_db(id_value, seller_name, price_entry, address_entry, province_entry, city_entry, zip_entry,
                       list_acc[4], list_acc[5], area_entry, status_entry, title_entry, list_acc[0])).pack()

def update_city_entry(event: "tk.Event[ttk.Combobox]", city_entry):
    selected_province = event.widget.get()
    cursor.execute("""SELECT prov_code FROM province_list WHERE prov_name = %s""", (selected_province,))
    province_code = cursor.fetchall()
   #print(province_code[0])
    cursor.execute(f'SELECT city_name FROM city_list WHERE prov_code=%s ORDER BY city_name',(province_code[0][0],))
    city_result = cursor.fetchall()
    city_list = [i[0] for i in city_result]
    city_entry.config(values=city_list)

def add_to_sell_db(entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entry10, entry11, entry12, entry13):
    for_insert = (entry1, entry2, entry3.get(), entry4.get(), entry5.get(), entry6.get(), 
                  entry7.get(), entry8, entry9, entry10.get(), entry11.get(), entry12.get(), str(entry13))
    insert_table_selling = """
    INSERT INTO lands_for_selling (land_id, seller_name, land_price, st_add, province_name, city_name, post_no,
        contact_number, email_info, size_sq_meters, title, status, acc_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    insert_table_buy = """
    INSERT INTO lands_for_buying (land_id, seller_name, land_price, st_add, province_name, city_name, post_no,
        contact_number, email_info, size_sq_meters, title, status, acc_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    cursor.execute(insert_table_selling, for_insert)
    cursor.execute(insert_table_buy, for_insert)
    conn.commit()

def view_sell_details(event):
      #cs = sell_list.curselection()
      w = event.widget
      index = w.selection()[0]
      value = w.item(index, "values")
      #print('You selected item %d: "%s"' % (index, value[0]))
      row_sell = f"SELECT * FROM lands_for_selling WHERE land_id = %s"
      cursor.execute(row_sell, (value[0],))
      row_sell = cursor.fetchall()
      #print(row_sell)

      top = Toplevel()
      top_sell_x, top_sell_y = window_config(500, 500, top)
      top.geometry(f'{500}x{500}+{top_sell_x}+{top_sell_y}')
      top.title(value[0])

      top_frame_sell = tk.Frame(top)
      top_frame_sell.pack()

      bottom_frame_sell = tk.Frame(top)
      bottom_frame_sell.pack()

      view_map_bot = tk.Button(bottom_frame_sell, font=button_font_style, text="View Map", command=lambda:combine_string_address(value[0]), bg="#FF2E97") 
      view_map_bot.pack(side = "left")
      edit_bot = tk.Button(bottom_frame_sell, font=button_font_style, text="Edit", command=lambda:edit_details(value[0]), bg="#FF2E97") 
      edit_bot.pack(side = "left")


def display_sell(sell_tree, list_acc):
    #sell_table.delete(0,END)
    
    cursor.execute(display_basic_info, (list_acc[0],))
    sell_result = cursor.fetchall()

    sell_table = listbox_header(sell_result, sell_tree)
    #print(sell_result)
    """ctr = 0

    for x in sell_result:
        sell_table.insert(END, x)
        ctr+=1"""
    sell_table.bind('<Double-1>', view_sell_details)

def edit_details(id_value):
    window = tk.Tk()
    window.title(f"Edit Value for {id_value}")
    window.resizable(False, False)
    x,y = window_config(400, 550, window)
    window.geometry(f'{400}x{550}+{x}+{y}')

    fillout_frame = tk.Frame(window, padx=18, pady=16) 
    fillout_frame.pack(fill="both", expand=True)
    

    tk.Label(fillout_frame, text="Selling Price:").pack(anchor="w", pady=(0,2)) 
    price_entry_edit = tk.Entry(fillout_frame)
    price_entry_edit.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Seller Contact Info:").pack(anchor="w", pady=(0,2)) 
    contact_entry_edit = tk.Entry(fillout_frame)
    contact_entry_edit.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Seller Email Info:").pack(anchor="w", pady=(0,2))
    email_entry_edit = tk.Entry(fillout_frame)
    email_entry_edit.pack(fill="x", pady=(0, 10))

    avail_not = ["Available", "Sold"]
    #opt = StringVar(value="Available")  
    tk.Label(fillout_frame, text="Status:").pack(anchor="w", pady=(0,2))
    status_entry_edit = ttk.Combobox(fillout_frame, values=avail_not)
    status_entry_edit.pack(fill="x", pady=(0, 10))

    tk.Button(fillout_frame, font=button_font_style, text="Confirm", command=lambda: update_sell_value(price_entry_edit, contact_entry_edit, email_entry_edit, status_entry_edit, id_value, window)).pack()


def update_sell_value(entry1, entry2, entry3, entry4, id_value, window_open):
    #for_update = (entry1.get(), entry2.get(), entry3.get(), entry4.get(), id_value)
    update_table_sell = f"""UPDATE lands_for_selling
                        SET land_price = '{entry1.get()}', contact_number = '{entry2.get()}', email_info = '{entry3.get()}', status = '{entry4.get()}'
                        WHERE land_id = {id_value};"""
    
    cursor.execute(update_table_sell)
    result = cursor.rowcount
    if result > 0:
        conn.commit()
        window_open.destroy()
    else:
        pass
