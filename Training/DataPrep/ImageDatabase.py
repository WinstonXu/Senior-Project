import os
import sqlite3

conn = sqlite3.connect('equations.db')
c = conn.cursor()

mnist_dir = 'DatasetPictures/MnistPics'
operators_dir = 'DatasetPictures/Operators'

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS mnist
             (filename TEXT PRIMARY KEY, number TEXT, used BOOLEAN)''')

count_dict = {}
for filename in os.listdir(mnist_dir):
    if '.jpg' in filename:
        number = filename.split("-")[1][0]

        # Insert a row of data
        c.execute("INSERT INTO mnist VALUES ('%s','%s',0)" % (filename, number))
        # Save (commit) the changes
        conn.commit()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS operators
             (filename TEXT PRIMARY KEY, operator TEXT, used BOOLEAN)''')

for filename in os.listdir(operators_dir):
    if '.jpg' in filename:
        operator = filename.split(" ")[0]
        # Insert a row of data
        c.execute("INSERT INTO operators VALUES ('%s','%s',0)" % (filename, operator))
        # Save (commit) the changes
        conn.commit()

conn.close()
