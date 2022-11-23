import mysql.connector
from mysql.connector import Error

def deleteOrder(connection,cursor): 
    foreign1= """ALTER TABLE Order_Details
                        DROP FOREIGN KEY Order_Details_ibfk_1, 
                        DROP FOREIGN KEY Order_Details_ibfk_3 """
    foreign2= """ALTER TABLE Order_Details
                ADD CONSTRAINT Order_Details_ibfk_1
                FOREIGN KEY (OrderID)
                REFERENCES Orders(OrderID)
                ON DELETE CASCADE, 
                ADD CONSTRAINT Order_Details_ibfk_3
                FOREIGN KEY (StatusID)
                REFERENCES Order_Details_Status(StatusID)
                ON DELETE CASCADE
                """
    foreign3= """ALTER TABLE Invoices
                        DROP FOREIGN KEY Invoices_ibfk_1"""
    foreign4= """ALTER TABLE Invoices
                ADD CONSTRAINT Invoices_ibfk_1
                FOREIGN KEY (OrderID)
                REFERENCES Orders(OrderID)
                ON DELETE CASCADE"""
    print("---------------------------")
    print("1. Delete by Order ID")
    print("2. Delete by Employee ID")
    print("3. Delete by Customer ID")
    print("4. Delete by Customer Name")
    userin=input("Type an option from above: ")
    valid = False
    while (valid==False): 
        while (not userin.strip().isdigit()): 
            userin =input("Must be a number between 1 and 4: ") 
        userin = int(userin.strip())
        if (userin<1 or userin>4): 
            valid=False
            userin =input("Must be a number between 1 and 4: ") 
        else: 
            valid=True

    try: 
        cursor.execute(foreign1)
        connection.commit()
        cursor.execute(foreign2)
        connection.commit()
        cursor.execute(foreign3)
        connection.commit()
        cursor.execute(foreign4)
        connection.commit()
    except Error as e: 
        print("There was a problem handling the foreign key altering, ",e)
        connection.rollback()

    if userin==1: 
        orderid=input("Enter the order ID: ")
        while (not orderid.strip().isdigit()): 
            orderid=input("Must be an integer: ")
        orderid = int(orderid)
        try: 
            
            Q1 = """DELETE FROM Order_Details WHERE OrderID={}""".format(orderid)
            Q2 = """DELETE FROM Invoices WHERE OrderID={}""".format(orderid)
            Q3 = """DELETE FROM Orders WHERE OrderID={}""".format(orderid)
            cursor.execute(Q1)
            connection.commit()
            print(cursor.rowcount, "Records related to order_details successfully deleted.") 
            cursor.execute(Q2) 
            connection.commit()
            print(cursor.rowcount, "Records related to Invoices successfully deleted.") 
            cursor.execute(Q3)
            connection.commit()
            print(cursor.rowcount, "Records related to Orders successfully deleted. ")

            return True

        except Error as e: 
            print("Error while deleting order ", e) 
            connection.rollback()
            return False
        
    if userin==2: 
        employeeid=input("Enter the employee ID: ")
        while (not employeeid.strip().isdigit()): 
            employeeid=input("Must be an integer: ")
        employeeid = int(employeeid.strip())
        try: 
            Q1 = """DELETE FROM Order_Details WHERE OrderID IN (SELECT OrderID FROM Orders WHERE EmployeeID={})""".format(employeeid)
            Q2 = """DELETE FROM Invoices WHERE OrderID IN (SELECT OrderID FROM Orders WHERE EmployeeID={})""".format(employeeid)
            Q3 = """DELETE FROM Orders WHERE EmployeeID={}""".format(employeeid)
            cursor.execute(Q1) 
            connection.commit()
            print(cursor.rowcount, "Records from Order Details successfully deleted. ")
            cursor.execute(Q2)
            connection.commit()
            print(cursor.rowcount, "Records from Invoices successfully deleted. ")
            cursor.execute(Q3) 
            connection.commit()
            print(cursor.rowcount, " Records from Orders successfully deleted. ")
            return True
        except Error as e: 
            print("Error while deleting order using employee id ", e)
            connection.rollback()
            return False 

    if userin==3: 
        customerid=input("Enter Customer ID: ") 
        while (not customerid.strip().isdigit()): 
            customerid=input("Must be an integer: ") 
        customerid= int(customerid.strip())
        try: 
            Q1 = """DELETE FROM Order_Details WHERE OrderID IN (SELECT OrderID FROM Orders WHERE CustomerID={})""".format(customerid)
            Q2 = """DELETE FROM Invoices WHERE OrderID IN (SELECT OrderID FROM Orders WHERE CustomerID={})""".format(customerid)
            Q3 = """DELETE FROM Orders WHERE CustomerID={}""".format(customerid)
            cursor.execute(Q1)
            connection.commit()
            print(cursor.rowcount, "Records from Order Details successfully deleted. ")
            cursor.execute(Q2) 
            connection.commit()
            print(cursor.rowcount, "Records from Invoices successfully deleted. ")
            cursor.execute(Q3)
            connection.commit()
            print(cursor.rowcount, "Records from Orders successfully deleted. ")
            connection.commit()
            return True
        except Error as e: 
            print("Error while deleting order using customer ID ", e)
            connection.rollback()
            return False
    
    #Deleting by Customer name
    if userin==4: 
        customername = input("Enter Customer Firstname and Lastname: ")
        customername = customername.split(" ")
        #Verify input
        while (len(customername)<2): 
            customername=input("Enter in First name AND Last Name (with space in between): ")
            customername.split(" ")
        firstname = customername[0]
        lastname = customername[1]
        try: 
            Q1 = """DELETE FROM Order_Details WHERE OrderID IN (SELECT OrderID FROM Orders
                WHERE CustomerID IN (SELECT ID FROM Customers
                WHERE FirstName='{}' AND LastName='{}')) """.format(firstname,lastname)

            Q2 = """DELETE FROM Invoices WHERE OrderID IN (SELECT OrderID FROM Orders
                WHERE CustomerID IN (SELECT ID FROM Customers 
                WHERE FirstName='{}' AND LastName='{}')) """.format(firstname,lastname)
                
            Q3 = """DELETE FROM Orders WHERE CustomerID IN 
                (SELECT ID FROM Customers
                WHERE FirstName='{}' AND LastName='{}')""".format(firstname, lastname)
            cursor.execute(Q1)
            connection.commit()
            print(cursor.rowcount, "Records from Order Details successfully deleted. ")
            cursor.execute(Q2)
            connection.commit()
            print(cursor.rowcount, "Records from Invoices successfully deleted. ")
            cursor.execute(Q3)
            print(cursor.rowcount, "Records from Orders successfully deleted. ")
            return True
        except Error as e: 
            print("Error while deleting order using customer name ", e)
            connection.rollback()
            return False

