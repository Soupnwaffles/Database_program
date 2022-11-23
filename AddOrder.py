import mysql.connector
from mysql.connector import Error

def addorder(connection, cursor): 
    try: 
        return 
    except Error as e: 
        print("Error when trying to add order, ",e)
        connection.rollback()
        return False