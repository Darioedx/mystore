import sqlite3


conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE productos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              product_name text, txt text, img1 text,img2 text, img3 text)''')
conn.commit()
conn.close()
