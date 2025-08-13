import tkinter as tk
import datetime
from datetime import datetime
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from window_config import window_config
from sql_database import connection
from view_map import *
from tkcalendar import DateEntry
from listbox import listbox_header


button_font_style = ("Arial", 12, "bold")
conn = connection()
cursor = conn.cursor()
display_basic_info="""select land_id, seller_name, land_price, province_name, contact_number, status from lands_for_buying;"""
create_table_sql_buying = """
CREATE TABLE IF NOT EXISTS lands_for_buying (
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

create_table_appointment_buying = """
CREATE TABLE IF NOT EXISTS lands_for_appointment (
    appointment_id VARCHAR(100) PRIMARY KEY,
    buyer_name VARCHAR(100) NOT NULL,
    new_land_id VARCHAR(100) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL
);
"""

cursor.execute(create_table_sql_buying)
cursor.execute(create_table_appointment_buying)

def display_buy(buy_tree, list_acc):
    #buy_table.delete(0,END)
    cursor.execute(display_basic_info)
    buy_result = cursor.fetchall()
        #print(sell_result)

    buy_result = listbox_header(buy_result, buy_tree)
    """ctr = 0

    for x in sell_result:
        buy_table.insert(END, x)
        ctr+=1"""
    buy_result.bind('<Double-1>', lambda event: view_buy_details(event, list_acc))

def view_buy_details(event, list_acc):
    w = event.widget
    index = w.selection()[0]
    value = w.item(index, "values")
    row_sell = f"SELECT * FROM lands_for_selling WHERE land_id = %s"
    cursor.execute(row_sell, (value[0],))
    row_sell = cursor.fetchall()

    top = Toplevel()
    top_sell_x, top_sell_y = window_config(500, 500, top)
    top.geometry(f'{500}x{500}+{top_sell_x}+{top_sell_y}')
    top.title(value[0])

    top_frame_buy = tk.Frame(top)
    top_frame_buy.pack()

    bottom_frame_buy = tk.Frame(top)
    bottom_frame_buy.pack()

    buyer_name  = list_acc[2] + ' ' + list_acc[1]

    view_map_bot = tk.Button(bottom_frame_buy, font=button_font_style, text="View Map", command=lambda:combine_string_address(value[0]), bg="#FF2E97") 
    view_map_bot.pack(side = "left")
    buy_bot = tk.Button(bottom_frame_buy, font=button_font_style, text="Set an Appointment", bg="#FF2E97", command=lambda:set_appointment_command(value[0], buyer_name)) 
    buy_bot.pack(side = "left")
    #rent_bot = tk.Button(bottom_frame_buy, font=button_font_style, text="Rent", bg="#FF2E97") 
    #rent_bot.pack(side = "left")

def buy_land(id_value, window_open):
    update_table_buy = f"""UPDATE lands_for_buying
                        SET status = 'Sold'
                        WHERE land_id = {id_value};"""
    cursor.execute(update_table_buy)
    conn.commit()
    window_open.destroy()
    """DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste';"""

def set_appointment_command(id_sell_land, buyer_name):
    window = tk.Tk()
    window.title("Set an appointment?")
    window.resizable(False, False)
    x,y = window_config(400, 550, window)
    window.geometry(f'{400}x{550}+{x}+{y}')

    fillout_frame = tk.Frame(window, padx=18, pady=16) 
    fillout_frame.pack(fill="both", expand=True)

    tk.Label(fillout_frame, text="ID:").pack(anchor="w", pady=(0,2)) 
    appointment_id = tk.Label(fillout_frame, text=id_sell_land)
    appointment_id.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Buyer Name:").pack(anchor="w", pady=(0,2)) 
    buy_name = tk.Label(fillout_frame, text=buyer_name)
    buy_name.pack(fill="x", pady=(0, 10))

    tk.Label(fillout_frame, text="Set Date:").pack(anchor="w", pady=(0,2)) 
    appointment_date_val = DateEntry(fillout_frame, width=12, background='darkblue', foreground='white', borderwidth=2,  date_pattern='yyyy-mm-dd')
    appointment_date_val.pack(pady=(0, 10))

    time_hr = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    tk.Label(fillout_frame, text="Set Time:").pack(anchor="w", pady=(0,2))
    hr_entry = ttk.Combobox(fillout_frame, values=time_hr)
    hr_entry.set("9:00")
    hr_entry.pack(pady=(0, 10))

    tk.Button(fillout_frame, font=button_font_style, text="Confirm", command=lambda: insert_to_appointments(appointment_id, buy_name, appointment_date_val, hr_entry, id_sell_land, window)).pack()

def insert_to_appointments(entry1, entry2, entry3, entry4, id, window_open):
    time_input = entry4.get().strip()
    print_time = datetime.strptime(time_input, '%H:%M').time()
    for_insert_appointment = (entry1.get(), entry2.get(), id, entry3.get(), print_time, entry3.get(), print_time, id)
    insert_lands_for_appointment = """
        INSERT INTO lands_for_appointment (
            appointment_id, buyer_name, new_land_id, appointment_date, appointment_time
        )
        SELECT %s, %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM lands_for_appointment
            WHERE appointment_date = %s AND appointment_time = %s AND new_land_id = %s
        );
        """
    count_table = """SELECT COUNT(*) FROM lands_for_appointment"""
    print(count_table)    
    cursor.execute(insert_lands_for_appointment, for_insert_appointment)
    result = cursor.rowcount
    #print("%d"%result)
    if result > 0:
        conn.commit()
        window_open.destroy()
    else:
        pass
    
