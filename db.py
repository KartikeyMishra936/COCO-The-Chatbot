import csv
import sqlite3

# Connect to database (creates the file if it doesn't exist)
con = sqlite3.connect("coco.db")

cursor = con.cursor()
# Create a table
#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))" 
#cursor.execute(query)
   # query = "INSERT INTO sys_command VALUES (null,'android studio','C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe')"
    #cursor.execute(query)
    #con.commit()
#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))" 
#cursor.execute(query)
#query = "INSERT INTO web_command VALUES (null,'chatgpt','https://chatgpt.com/')"
#cursor.execute(query)
#con.commit()
#app_name = "android studio"
#cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
#result = cursor.fetchall()
#print(result[0][0])
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')
# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
#desired_columns_indices = [0, 18]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    #csvreader = csv.reader(csvfile)
    #for row in csvreader:
        #selected_data = [row[i] for i in desired_columns_indices]
        #cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
#con.commit()
#con.close()
#query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890')"
#cursor.execute(query)
#con.commit()
query = 'Maa'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0])