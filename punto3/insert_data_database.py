import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('Rtramite.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define the values to insert into the table
values = [
    ('EMT219', 'Jose Gómez', 1001915145),
    ('JGO954', 'Juan Albis', 1001915463),
    ('DTW486', 'Carlos Recio', 1001917156)
]

# Insert the values into the table
cursor.executemany('INSERT INTO mytable (placa, nombre, cc) VALUES (?, ?, ?)', values)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
