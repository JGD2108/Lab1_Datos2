import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the table with the specified columns
cursor.execute('''CREATE TABLE mytable (
                placa TEXT,
                nombre TEXT,
                cc INTEGER
                )''')

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
