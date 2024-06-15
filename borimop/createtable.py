import sqlite3

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE books (name TEXT, author TEXT, year TEXT)')
print("Created table successfully!")

conn.close()