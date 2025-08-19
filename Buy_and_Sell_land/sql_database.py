"""
SQL Database Connection Module

This module provides a function to establish a connection to the 
MySQL database used in the Land Buy & Sell application.

Modules:
    - mysql.connector: For connecting to the MySQL database

Author: Angelo Matthew Quilapio
License: All Rights Reserved
"""
import mysql.connector

def connection():
    """
    Establish a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: 
            A connection object to interact with the database
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="W@7la8zu",
        database="buy_sell_db"
    )
    return conn