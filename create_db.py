import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", 
    user="root", 
    passwd="mysql42dbpff"
)

my_cursor = mydb.cursor()
#my_cursor.execute("CREATE DATABASE movies")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)