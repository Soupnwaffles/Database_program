import mysql.connector
from mysql.connector import Error

def printPendingOrder(connection, cursor): 
    try: 
        Q1 = """SELECT DISTINCT * FROM Orders WHERE ShippedDate IS NULL"""
        cursor.execute(Q1)
        connection.commit()
        rows = cursor.fetchall()
        print("""(OrderID, EmployeeID, CustomerID, OrderDate, ShippedDate, 
            ShipperID, ShipName, ShipAddress, ShipCity, ShipState, ShipZIP, ShipCountry, ShippingFee, Taxes
            PaymentType, PaidDate, Notes, TaxRate,TaxStatus, StausID)""")
        for tuple in rows: 
            print(tuple)
        return True
    except Error as e: 
        print("Problem when trying to print pending order, ",e)
        connection.rollback()
        return False
    return 