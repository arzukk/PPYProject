import sqlite3
connection = sqlite3.connect("Books.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Books")
results = cursor.fetchall()
for row in results:
    print(row)
connection.close()
