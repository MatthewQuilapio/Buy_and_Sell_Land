import webbrowser
import urllib.parse
from sql_database import connection

conn = connection()
cursor = conn.cursor()

def combine_string_address(id_value):
    address_query = f"SELECT st_add, province_name, city_name FROM lands_for_selling WHERE land_id = %s"
    cursor.execute(address_query, (id_value,))
    address_result = cursor.fetchall()
    full_address_list = [item for t in address_result for item in t]
    full_address = full_address_list[0] + ' ' + full_address_list[2] + ', ' + full_address_list[1]


    query = urllib.parse.quote(full_address)


    url = f"https://www.google.com/maps/search/?api=1&query={query}"


    webbrowser.open(url)