import mysql.connector


def connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="W@7la8zu",
        database="buy_sell_db"
    )
    return conn