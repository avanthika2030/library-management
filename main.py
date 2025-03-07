import mysql.connector
import datetime

# Database Connection
db = mysql.connector.connect(host='localhost', user='root', passwd='avk2030')
mycursor = db.cursor()

# Create Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS Library_management1")
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='avk2030',
        database='Library_management1'
    )
#db = connect_db()
db = connect_db()
mycursor = db.cursor()

# Creating Tables
mycursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    bregno INT(7) PRIMARY KEY,
    bname VARCHAR(50),
    author VARCHAR(50),
    genre VARCHAR(30),
    publiname VARCHAR(50),
    nocopy INT(6),
    shelfno INT(4)
)
""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS customer (
    ccode INT(7) PRIMARY KEY,
    cname VARCHAR(50),
    cphno VARCHAR(20),
    membno INT(7),
    memexpire DATE
)
""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(40) PRIMARY KEY,
    passwd VARCHAR(60)
)
""")

# Inserting Books
qry1 = "INSERT IGNORE INTO books (bregno, bname, author, genre, publiname, nocopy, shelfno) VALUES (%s,%s,%s,%s,%s,%s,%s)"
data1 = [
    (5566, 'Cinderella', 'Daisy Fisher', 'Fiction', 'Nootan Saral', 100, 12),
    (6455, 'Wings of Fire', 'A. P. J. Abdul Kalam', 'Biography', 'AKM', 100, 15),
    (2349, 'Inferno', 'Dan Brown', 'Fiction', 'Wellwishers', 50, 20),
    (5749, 'Diary of a Wimpy Kid', 'Jeff Kinney', 'Fiction', 'Chashers', 50, 19),
    (4989, 'Harry Potter and the Cursed Child', 'J.K. Rowling', 'Thriller', 'Bhoomi', 30, 15)
]
mycursor.executemany(qry1, data1)

# Inserting Users
qry3 = "INSERT IGNORE INTO users (username, passwd) VALUES (%s, %s)"
data3 = [
    ('kish@13', 'kish133'),
    ('gobi@98', 'gobi98'),
    ('hima@32', 'hima32'),
    ('avn2030', 'avn@2030')
]
mycursor.executemany(qry3, data3)

db.commit()
mycursor.close()
db.close()

#Description
def description():
    myfile=open("description.txt","r")
    contents=myfile.read()
    print(contents)
    print()
    print('--------'*20)


#Add books
def add_stock():
    db = connect_db()
    mycursor = db.cursor()

    while True:
        print("\nADD NEW BOOK")
        bregno = int(input("Enter Book Number: "))
        bname = input("Enter Book Name: ")
        author = input("Enter Author Name: ")
        genre = input("Enter Genre (Fiction/Non-fiction/Biography): ")
        publiname = input("Enter Publisher Name: ")
        nocopy = int(input("Enter Number of Copies: "))
        shelfno = int(input("Enter Shelf Number: "))

        query = "INSERT INTO books (bregno, bname, author, genre, publiname, nocopy, shelfno) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(query, (bregno, bname, author, genre, publiname, nocopy, shelfno))
        db.commit()
        print("Book Added Successfully!")

        choice = input("Do you want to add another book? (y/n): ").lower()
        if choice != 'y':
            break

    mycursor.close()
    db.close()

#Mainmenu
def mainmenu():
    print('********'*18)
    print()
    l=" LIBRARY MANAGMENT "
    print("{:^89}".format(l))
    print('********'*18)
    print('********'*18)
    print()
    print()
    print()
    print('~~~~~~~~'*18)
    print()
    print("1.Book stock")
    print("2.customer details")
    print("3.exit")
    ch1=int(input("Enter your choice[1/2/3]:"))


#Register
def newuser():
    db = connect_db()
    mycursor = db.cursor()

    while True:
        usern = input("Enter a new username: ")

        # Check if the username already exists
        mycursor.execute(f"SELECT username FROM users WHERE username = '{usern}'")
        check = mycursor.fetchone()
        if check:
            print("Username already exists. Try a different one.")
            continue
        
        passwd = input("Enter password: ")
        passwd1 = input("Confirm password: ")

        if passwd == passwd1:
            query = "INSERT INTO users (username, passwd) VALUES (%s, %s)"
            mycursor.execute(query, (usern, passwd))
            db.commit()
            print("User Registered Successfully!")
            break
        else:
            print("Passwords do not match! Try again.")

    mycursor.close()
    db.close()



#Login
def login():
    db = connect_db()
    mycursor = db.cursor()

    user = input("Enter Username: ")
    passwrd = input("Enter Password: ")

    mycursor.execute(f"SELECT * FROM users WHERE username='{user}' AND passwd='{passwrd}'")
    result = mycursor.fetchone()

    if result:
        print("Login Successful! Welcome, ", user)
        return True
    else:
        print("Invalid Username or Password!")
        return False


#Menu
def menu():
    print()
    print("1.Register")
    print("2.Login")
    print("3.Exit")

#Insert customer
def newcust(): #done
    db = connect_db()
    mycursor = db.cursor()
    while True:
        print("\nWELCOME TO DREAMS BOOKS MANAGEMENT")
        print("Please enter the following details to proceed:")
        ccode = int(input("Enter customer code: "))
        cname = input("Enter customer name: ")
        cphno = input("Enter your contact number: ")
        membno = int(input("Enter membership number: "))
        memexpire = input("Enter date of membership expiry [YYYY-MM-DD]: ")
        
        query = "INSERT INTO customer (ccode, cname, cphno, membno, memexpire) VALUES (%s, %s, %s, %s, %s)"
        data = (ccode, cname, cphno, membno, memexpire)
        
        try:
            mycursor.execute(query, data)
            db.commit()
            print("Inserted successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        if input("Do you want to add more? [y/n]: ").lower() != 'y':
            break
    
    mycursor.close()
    db.close()
    mainmenu()

#Book update
def update_book():#done
    db = connect_db()    
    mycursor = db.cursor()
    
    while True:
        print("\n UPDATE BOOK ")
        print('-------------')

        try:
            bno = int(input("Enter book number: ").strip())
        except ValueError:
            print("Invalid input! Please enter a valid book number.")
            continue

        print("\nMENU")
        print("---------")
        print("1. Book Name")
        print("2. Number of Copies")
        print("3. Publisher")
        
        try:
            choice = int(input("What do you want to change? [1/2/3]: ").strip())
        except ValueError:
            print("Invalid choice! Please enter a valid option.")
            continue

        if choice == 1:
            nbook = input("Enter the new name of the book: ").strip()
            query = "UPDATE books SET bname = %s WHERE bregno = %s"
            data = (nbook, bno)

        elif choice == 2:
            try:
                ncopies = int(input("Enter the new number of copies: ").strip())
            except ValueError:
                print("Invalid input! Please enter a valid number.")
                continue
            query = "UPDATE books SET nocopy = %s WHERE bregno = %s"
            data = (ncopies, bno)

        elif choice == 3:
            npubli = input("Enter the new publisher: ").strip()
            query = "UPDATE books SET publiname = %s WHERE bregno = %s"
            data = (npubli, bno)

        else:
            print("Invalid choice! Please enter a number between 1 and 3.")
            continue

        mycursor.execute(query, data)
        db.commit()
        print("\n✅ Record Updated Successfully!")

        c = input("Do you want to update more? [y/n]: ").strip().lower()
        if c == 'n':
            return mainmenu()


#Customer update
def update_cust(): #done
    db = connect_db()
    mycursor = db.cursor()
    while True:
        print("\nUPDATE CUSTOMER")
        cno = int(input("Enter customer code: "))
        print("1. Customer name\n2. Phone number\n3. Membership expiry date")
        choice = int(input("What do you want to change? [1/2/3]: "))
        
        if choice == 1:
            ncust = input("Enter new name: ")
            query = "UPDATE customer SET cname=%s WHERE ccode=%s"
            data = (ncust, cno)
        elif choice == 2:
            nphno = input("Enter new phone number: ")
            query = "UPDATE customer SET cphno=%s WHERE ccode=%s"
            data = (nphno, cno)
        elif choice == 3:
            nexpiry = input("Enter new expiry date [YYYY-MM-DD]: ")
            query = "UPDATE customer SET memexpire=%s WHERE ccode=%s"
            data = (nexpiry, cno)
        else:
            print("Invalid choice!")
            continue
        
        mycursor.execute(query, data)
        db.commit()
        print("Record updated successfully!")
        
        if input("Do you want to update more? [y/n]: ").lower() != 'y':
            break
    
    mycursor.close()
    db.close()
    mainmenu()

#Membership status
def memcheck(): #done
    db = connect_db()
    mycursor = db.cursor()
    print("\nMEMBERSHIP STATUS")
    try:
        mcode = int(input("Enter membership code: "))
        mycursor.execute("SELECT memexpire FROM customer WHERE membno=%s", (mcode,))
        res = mycursor.fetchone()
        
        if res:
            expiry_date = datetime.strptime(res[0], "%Y-%m-%d")
            today_date = datetime.today()
            if expiry_date <= today_date:
                print("Membership has expired!")
            else:
                print("Membership is active!")
        else:
            print("Membership code not found!")
    except Exception as e:
        print(f"Error: {e}")
    
    mycursor.close()
    db.close()




#Delete book
def bdelete(): #done
    try:
        db = connect_db()
        mycursor = db.cursor()
        
        while True:
            print("\n DELETE BOOK ")
            print('-------------')
            
            try:
                bno = int(input("Enter book number to be deleted: "))
                mycursor.execute("DELETE FROM books WHERE bregno = %s", (bno,))
                db.commit()
                
                if mycursor.rowcount == 0:
                    print("Record not found. Please enter a valid book number.")
                else:
                    print("Record deleted successfully.")
            
            except ValueError:
                print("Invalid input. Please enter a valid book number.")
            
            c = input("\nDo you want to delete more? [y/n]: ").strip().lower()
            if c != 'y':
                break

    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
    
    finally:
        mycursor.close()
        db.close()


#Delete customer
def cdelete(): #done
    db = connect_db()
    mycursor = db.cursor()
    while True:
        print("\nDELETE CUSTOMER")
        cno = int(input("Enter customer code to be deleted: "))
        
        mycursor.execute("DELETE FROM customer WHERE ccode=%s", (cno,))
        db.commit()
        
        if mycursor.rowcount == 0:
            print("Record not found!")
        else:
            print("Record deleted successfully!")
        
        if input("Do you want to delete more? [y/n]: ").lower() != 'y':
            break
    
    mycursor.close()
    db.close()
    mainmenu()


#Search customer

def search(): #done
    try:
        db = connect_db()
        mycursor = db.cursor()
        
        while True:
            print("\n SEARCH CUSTOMER ")
            print('-----------------')
            
            try:
                cno = int(input("Enter customer code: "))
                mycursor.execute("SELECT * FROM customer WHERE ccode = %s", (cno,))
                result = mycursor.fetchone()
                
                if result:
                    print("\nCustomer details found:")
                    print("Name of the customer:", result[1])
                    print("Phone number:", result[2])
                    print("Membership number:", result[3])
                    print("Membership expiry date:", result[4])
                else:
                    print("\nNo record found.")
            
            except ValueError:
                print("Invalid input. Please enter a valid customer code.")
            
            c = input("\nDo you want to search more? [y/n]: ").strip().lower()
            if c != 'y':
                break

    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
    
    finally:
        mycursor.close()
        db.close()



def display(): #done
    """Function to display books based on genre, author, or all records."""
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='avk2030',
        database='Library_management1'
    )
    mycursor = db.cursor()

    try:
        while True:
            print("\n DISPLAY BOOKS ")
            print('---------------')
            print('1. Display by Genre')
            print('2. Display by Author')
            print('3. Display All Records')
            print('4. Return to Main Menu')

            try:
                opt = int(input("Enter choice: "))

                if opt == 1:
                    gen = input("Enter genre [fiction/nonfiction/biography]: ").strip().lower()
                    mycursor.execute("SELECT * FROM books WHERE genre = %s", (gen,))
                
                elif opt == 2:
                    auth = input("Enter author full name: ").strip()
                    mycursor.execute("SELECT * FROM books WHERE author = %s", (auth,))
                
                elif opt == 3:
                    mycursor.execute("SELECT * FROM books")
                
                elif opt == 4:
                    return mainmenu()
                
                else:
                    print("Invalid choice. Please enter a valid option.")
                    continue  # Go back to the menu
                
                # Fetch results
                records = mycursor.fetchall()
                if not records:
                    print("No records found.")
                    continue
                
                # Display header
                print('\n' + '~~~~~~~~~~' * 18)
                print(f"{'Book No':<10} {'Book Name':<40} {'Author':<25} {'Genre':<16} {'Publisher':<21} {'Quantity':<10} {'Shelf No'}")
                print('~~~~~~~~~~' * 18)

                # Display books
                for record in records:
                    print(f"{record[0]:<10} {record[1]:<40} {record[2]:<25} {record[3]:<16} {record[4]:<21} {record[5]:<10} {record[6]}")
                    print('~~~~~~~~~~' * 18)
                
            except ValueError:
                print("Invalid input. Please enter a number between 1-4.")
                continue  # Restart loop

            # Ask if the user wants to continue
            c = input("\nDo you want to display more? [y/n]: ").strip().lower()
            if c != 'y':
                break

    except mysql.connector.Error as e:
        print("Error accessing the database:", e)

    finally:
        mycursor.close()
        db.close()


def main():
    print('---------' * 18)
    print()
    m = " WELCOME TO DREAMS BOOKS MANAGEMENT "
    print("{:^85}".format(m))
    print('~~~~~~~~~' * 18)
    print('*********' * 18)
    print()
    
    description()

    while True:
        menu()
        ch = input("Enter your choice [1/2/3]: ").strip()

        if ch == '1':
            newuser()

        elif ch == '2':
            if login():
                while True:
                    mainmenu()
                    ch1 = input("Confirm your choice [1/2/3]: ").strip()

                    if ch1 == '1':  # Book Stock Management
                        print("\n{:^85}".format("BOOK STOCK"))
                        print('~~~~~~~~' * 18)
                        print("\n1. Add New Stock\n2. Update Stock\n3. Delete Stock\n4. Display Stock\n5. Exit")
                        
                        ch2 = input("Enter choice: ").strip()
                        if ch2 == '1':
                            add_stock()
                        elif ch2 == '2':
                            update_book()
                        elif ch2 == '3':
                            bdelete()
                        elif ch2 == '4':
                            display()
                        elif ch2 == '5':
                            print("Thank you!")
                            break
                        else:
                            print("Invalid entry. Please try again.")

                    elif ch1 == '2':  # Customer Management
                        print("\n{:^85}".format("CUSTOMER DETAILS"))
                        print('~~~~~~~~' * 18)
                        print("\n1. Add Customer\n2. Update Customer\n3. Delete Customer")
                        print("4. Membership Status\n5. Search Customer\n6. Exit")
                        
                        ch3 = input("Enter choice: ").strip()
                        if ch3 == '1':
                            newcust()
                        elif ch3 == '2':
                            update_cust()
                        elif ch3 == '3':
                            cdelete()
                        elif ch3 == '4':
                            memcheck()
                        elif ch3 == '5':
                            search()
                        elif ch3 == '6':
                            break
                        else:
                            print("Invalid entry. Please try again.")

                    elif ch1 == '3':
                        print("Have a nice day!")
                        break

                    else:
                        print("Invalid entry. Please try again.")
                        break

        elif ch == '3':
            print("Have a nice day!")
            quit()

        else:
            print("Invalid entry. Please try again.")

if __name__ == "__main__":
    main()
