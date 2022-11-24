import mysql.connector
from mysql.connector import Error

from dbapp import addcustomer

def addorder(connection, cursor): 
    try: 
        userin= input("Enter employee ID: ") 
        while (intcheck(userin) == False): 
            userin= input("Must be an integer: ") 
        userin=int(userin.strip())
        employeeid = userin
        Q = f"""SELECT * FROM Employees WHERE ID={employeeid}"""
        cursor.execute(Q)
        connection.commit()
        if (cursor.rowcount<1): 
            employeeid = 3
    

        # Enter in customer name
        #ship_name is full name of customer
        #customername is array with ['Firstname', 'Lastname']
        ship_name=input("Enter Customer Full Name : ")
        ship_name = str(ship_name)
        while (len(ship_name)< 3): 
            ship_name=input("Must be Firstname (space) Lastname: ")
            ship_name=str(ship_name)
        customername=str(ship_name).split(" ")
        while len(customername) < 2: 
            ship_name=input("Enter First and Last Name: ")
            customername=ship_name.split(" ") 
        # Check if customer already exists
        Q = f"""SELECT * FROM Customers WHERE Firstname='{customername[0]}' AND Lastname='{customername[1]}' """
        cursor.execute(Q)
        connection.commit()
        #If customer doesn't exist, add customer
        if int(cursor.rowcount) < 1:
            print("Customer does not exist in Database, enter your info: ")
            addcustomer(connection, cursor, customername)

        # GET Customer ID 
        Q = f"""SELECT ID FROM Customers WHERE Firstname='{customername[0]}' AND Lastname='{customername[1]}' """
        cursor.execute(Q)
        connection.commit()
        result = cursor.fetchall()
        t= result[0]
        customerid=int(t[0])
        
        #Asks for shipperID, defaults to 1 
        shipperid = input("Enter 1,2,3 for shipping company A, B or C: ")
        if (shipperid.strip() != "1" or shipperid.strip() != "2" or shipperid.strip() != "3"): 
            shipperid = 1 
        else: 
            shipperid = int(shipperid.strip())

        #Tax exempt
        taxstatus= 0
        taxrate = 0 
        taxes = 0 

        #Getting Address, City, State, ZIP and Country
        Q=f"""SELECT Address FROM Customers WHERE Firstname='{customername[0]}' AND Lastname='{customername[1]}'"""
        print(customername[0], customername[1])
        cursor.execute(Q)
        connection.commit()
        result=cursor.fetchall()
        t = result[0]
        shipaddress=t[0]

        Q=f"""SELECT City FROM Customers WHERE Firstname='{customername[0]}' AND Lastname='{customername[1]}'"""
        print("CITY: ", customername[0])
        cursor.execute(Q)
        connection.commit()
        result=cursor.fetchall()
        t = result[0]
        shipcity=t[0]

        Q=f"""SELECT State FROM Customers WHERE Firstname='{customername[0]}' AND Lastname='{customername[1]}'"""
        print("State pass: ")
        cursor.execute(Q)
        connection.commit()
        result=cursor.fetchall()
        t = result[0]
        shipstate=t[0]

        Q=f"""SELECT ZIP FROM Customers WHERE Firstname='{customername[0]}' AND Lastname='{customername[1]}'"""
        print("zip pass: ")
        cursor.execute(Q)
        connection.commit()
        result=cursor.fetchall()
        t = result[0]
        zip=t[0]

        Q=f"""SELECT Country FROM Customers WHERE Firstname='{customername[0]}' AND Lastname='{customername[1]}'"""
        print("Country pass: ")
        cursor.execute(Q)
        connection.commit()
        result=cursor.fetchall()
        t = result[0]
        country=t[0]

        shippingfee=0
        notes = None 
        statusid = 0

        paymenttype= None
        paiddate=None
        shippeddate = None
        shipname=None

        print(f"""({employeeid}, {customerid}, CURDATE(), {shippeddate}, 
                            {shipperid}, '{shipname}', '{shipaddress}', '{shipcity}', '{shipstate}',
                             '{zip}', '{country}', {shippingfee}, {taxes}, {paymenttype},
                              {paiddate}, {notes}, {taxrate}, {taxstatus}, {statusid})""")

        Q = f"""INSERT INTO Orders(EmployeeID, CustomerID, OrderDate, ShippedDate,
                                            ShipperID, ShipName, ShipAddress, ShipCity, ShipState,
                                            ShipZIP, ShipCountry, ShippingFee, Taxes, PaymentType, 
                                            PaidDate, Notes, TaxRate, TaxStatus, StatusId) 
                            VALUES ( 
                            {employeeid}, {customerid}, CURDATE(), {shippeddate}, 
                            {shipperid}, '{shipname}', '{shipaddress}', '{shipcity}', '{shipstate}',
                             '{zip}', '{country}', {shippingfee}, {taxes}, {paymenttype},
                              {paiddate}, {notes}, {taxrate}, {taxstatus}, {statusid})"""
        cursor.execute(Q)
        connection.commit()
        print(cursor.rowcount, "Records were added to Orders. ")
        
        return True
    except Error as e: 
        print("Error when trying to add order, ",e)
        connection.rollback()
        return False

def intcheck(userinput): 
    try: 
        userint=int(userinput)
        return True 
    except: 
        print("Your input is not an integer ")
        return False 