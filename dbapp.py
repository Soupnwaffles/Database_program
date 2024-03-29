import mysql.connector
from mysql.connector import Error
import DeleteOrder as d
import AddOrder as ao
import PrintPending as p
import getpass

# Prompted for info, one at a time
    #ID's auto generated (biggest existing num + 1)
    #MySQL has LAST_INSERT_ID() to obtain auto-increment val after insert

    #Populate proper info
    #(list price, order date, ship address) To: 
    # ORDERS and ORDER_DETAILS

def main():
    try: 
        print("Default host='localhost', user='root', password='' ")
        print("1 : Enter own user, pass, host for mysql")
        print("Anything else: Uses default user, pass, and host")
        usercredbool = input("Select (type) option: ")
        if usercredbool.strip() == "1": 
            username = input("Enter username: ")
            passwrd = getpass.getpass('Enter (hidden) password: ')
            hostserv = input("Enter host: ")
            print("\nMay take a while if host info is wrong, please wait. ")
            try: 
                connection = mysql.connector.connect(host=hostserv, database='northwind', user=username, password=passwrd)
            except Error as e: 
                print("mysql login info incorrect, ", e)
                return False
        # Connect to mysql
        else: 
            connection = mysql.connector.connect(host='localhost', 
                                            database='northwind',
                                            user='root', password='')
        # Check if connection is established
        if connection.is_connected(): 
            cursor =connection.cursor(buffered=True)
            printuserprompt()
            userin =input("Pick one of the above, type: q, quit, exit, or 7 to exit: ")
            if (quitcheck(userin) or userin.strip() == "7"): 
                connection.rollback()
                cursor.close()
                connection.close()
                return 
            else: 
                while (intcheck(userin, True) == False): 
                    printuserprompt()
                    userin= input("Must be a number between (including) 1 and 7: ")
                userin = int(userin.strip()) 
                if (userin==7): 
                    connection.rollback()
                    cursor.close()
                    connection.close()
                    return 
                elif (userin==1): 
                    addcustomer(connection,cursor)

                elif (userin==2): 
                    print("Add order") 
                    ao.addorder(connection,cursor)
                elif (userin==3): 
                    print("remove order") 
                    d.deleteOrder(connection, cursor)

                elif (userin==4): 
                    print("Ship an order")
                elif (userin==5): 
                    print("print pending orders") 
                    p.printPendingOrder(connection, cursor)
                elif (userin==6): 
                    print("more options")
        else: 
            print("Connection did not work")
            return False
            
                
    except Error as e: 
        print("Error while connecting to MySQL", e) 
        connection.rollback()
    finally: 
        try: 
            if connection.is_connected(): 
                cursor.close()
                connection.close()
        except: 
            print("Connection wasn't established, stopped program. ")
            return 
    return 

def addcustomer(connection, cursor, usein=None): 
    #Simply do an insert for customer.
    #Uses checks for varchars for length
    company = input("Enter company name: ")
    while (varcharcheck(company,50)==False): 
        company = input("Company must be within 50 characters: ")
    if quitcheck(company)== True: 
        return False 
    if usein ==None:
        lastname= input("Enter last name: ")
        while (varcharcheck(lastname,50)==False): 
            lastname= input("Last name must be within 50 characters: ")
        if quitcheck(lastname): 
            return False
    else: 
        lastname=usein[1]
    
    if usein == None: 
        firstname= input("Enter first name: ")
        while (varcharcheck(firstname,50)==False): 
            firstname=input("First name must be within 50 chars: ")
        if quitcheck(firstname): 
            return False
    else: 
        firstname=usein[0]
    email= input("Enter email address: ") 
    while (varcharcheck(email,50)==False): 
        email=input("Email must be within 50 characters: ")
    if quitcheck(email): 
        return False
    jobtitle= input("Enter job title: ")
    while(varcharcheck(jobtitle, 50)==False):
        jobtitle=input("Job title must be w/in 50 chars: ") 
    if quitcheck(jobtitle): 
        return False
    businessphone = input("Enter business phone number: ")
    while(varcharcheck(businessphone,25)==False): 
        businessphone=input("Phone number must be less than 25 characters long: ")
    if quitcheck(businessphone): 
        return False
    
    homephone = input("Enter home phone number: ")
    while(varcharcheck(homephone,25)==False): 
        homephone=input("home phone number must be less than 26 characters: ")
    if quitcheck(homephone): 
        return False
    mobilephone = input("Enter mobile phone number: ")
    while(varcharcheck(mobilephone,25)==False): 
        mobilephone=input("mobile phone number must be less than 26 characters: ")
    if quitcheck(mobilephone): 
        return False
    fax = input("Enter fax: ")
    while(varcharcheck(fax,25)==False): 
        fax = input("fax must be less than 25 characters: ")
    if quitcheck(fax): 
        return False
    address = input("Enter Address: ")
    if quitcheck(address): 
        return False
    city = input("Enter City: ")
    while (varcharcheck(city,50)==False): 
        city=input("city must be less than 51 chars long: ")
    if quitcheck(city): 
        return False
    state = input("Enter state: ")
    while(varcharcheck(state,50)==False): 
        state=input("state must be at most 50 chars: ")
    if quitcheck(state): 
        return False
    zip = input("Enter zipcode: ")
    while(varcharcheck(zip,15)==False): 
        zip=input("zip must be less than 16 chars long, enter again: ")
    if quitcheck(zip): 
        return False
    country = input("Enter Country: ")
    while(varcharcheck(country, 50)==False): 
        country=input("Country length must be less than 51 chars long: ")
    if quitcheck(country): 
        return False
    web = input("Enter web info, or nothing: ")
    if quitcheck(web): 
        return False
    
    notes = input("Enter notes: ")
    if quitcheck(notes): 
        return False
    attachments = input("Enter any attachments: ")
    if quitcheck(attachments): 
        return False
    
    try: 
        myquery = """INSERT INTO Customers (Company, LastName, FirstName, Email, JobTitle,
         BusinessPhone, HomePhone, MobilePhone, 
         Fax, Address, City, State, ZIP, Country,
        Web, Notes, Attachments)
        VALUES ( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' )
        """.format(company,lastname,firstname,email,jobtitle,businessphone,homephone,mobilephone,fax,address,city,state,zip,country,web,notes,attachments)

        cursor.execute(myquery)
        connection.commit()
        print(cursor.rowcount, "Record successfully inserted into Customers") 
        return True
    except Error as e: 
        print("Error while adding to Customers ", e) 
        connection.rollback()
        return False

    return True

def addorder(connection, cursor): 
    # Pay attention to foreign key constraints on: 
    # Customer, Employee, Shipper,Product,OrderID,etc
    # Multiple products can be placed in an order 
    # Order rejected if a product in the order is discontinued

    # My notes: 
    #ask consecutively what is each var
    # Send to ORDERS and ORDER_DETAILS
        # Except errors if not valid, give message. 
    # Pay attention to foreign keys. 
    # Allow for multiple products. 
        # Ask if another product
    # IF order is discontinued, rollback
    return 


def printuserprompt(): 
    print("1. add a customer")
    print("2. add an order")
    print("3. remove an order")
    print("4. ship an order")
    print("5. print pending orders (not shipped yet) with customer information")
    print("6. more options")
    print("7. exit")
    return 

def varcharcheck(userinput, length=None): 
    if (length != None and len(userinput)> length): 
        return False
    return True 

def intcheck(userinput, start=None): 
    try: 
        userint=int(userinput)
        if (start==True and (userint>7 or userint<1)):
            return False 
        return True 
    except: 
        print("Your input is not an integer ")
        return False 

def quitcheck(userinput): 
    if (userinput.lower().strip() == "q" or 
        userinput.lower().strip() == "quit" or
        userinput.lower().strip() == "exit"):
        return True
    else: 
        return False
if __name__ == "__main__": 
    main()
