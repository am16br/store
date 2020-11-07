import sqlite3  #importing sqlite3

con = sqlite3.connect('products.db') #connecting to/creating/opening database
print ("Opened database successfully")

cur = con.cursor()                     #setting cursor
cur.execute('''CREATE TABLE Products (
                    Name TEXT,
                    Price REAL,
                    Description TEXT,
                    Small INTEGER,
                    Medium INTEGER,
                    Large INTEGER,
                    XL INTEGER,
                    Type TEXT,
                    Image BLOB)''')
print ("Products Table created successfully")

cur.execute('''CREATE TABLE SiteInfo (
                    Name TEXT,
                    Email TEXT,
                    Address TEXT,
                    PhoneNumber TEXT,
                    About TEXT)''')
print ("SiteInfo Table created successfully")

cur.execute('''CREATE TABLE Services (
                    Name TEXT,
                    Price REAL,
                    Time TEXT,
                    Description TEXT,
                    Type TEXT,
                    Image BLOB)''')
print ("Services Table created successfully")

cur.execute('''CREATE TABLE Cart (
                    ItemNum INTEGER,
                    Name TEXT,
                    Price REAL,
                    Size TEXT,
                    Quantity INTEGER,
                    Total REAL,
                    Image BLOB)''')
print ("Cart Table created successfully")

cur.execute('''CREATE TABLE Subscribers (
                    Email TEXT)''')
print ("Subscribers Table created successfully")

cur.execute('''CREATE TABLE Contact (
                    FName TEXT,
                    LName TEXT,
                    Email TEXT,
                    Subject TEXT,
                    Message TEXT)''')
print ("Contact Table created successfully")

cur.execute('''CREATE TABLE Orders (
                    FName TEXT,
                    LName TEXT,
                    Address TEXT,
                    State TEXT,
                    Zip TEXT
                    ProductsOption TEXT)''')
print ("Orders Table created successfully")

con.close() #closing database
