import mysql.connector
from mysql.connector import Error

def printPendingOrder(connection, cursor): 
    try: 
        Q1 = """SELECT DISTINCT * FROM Orders WHERE ShippedDate IS NULL ORDER BY OrderDate"""
        cursor.execute(Q1)
        connection.commit()
        rows = cursor.fetchall()
        print("Pending Orders: ") 
        for tuple in rows: 
            print("Order Date: "+ str(tuple[3]))
            print("Order ID: "+ str(tuple[0])," | ", "Customer ID: "+ str(tuple[2]), " | ", "Employee ID: "+ str(tuple[1])) 
            print("Shipper ID: " + str(tuple[5])," | ", "Name: " + str(tuple[6]))
            print("Shipping address: " + str(tuple[7]), " | ", "Shipping state: "+ str(tuple[9]))
            print("-----------------------------------------------------------------")
        return True
    except Error as e: 
        print("Problem when trying to print pending order, ",e)
        connection.rollback()
        return False
    return False