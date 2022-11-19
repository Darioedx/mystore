import sqlite3


conn = sqlite3.connect('database.db')
c = conn.cursor()
x = "perro"
# Create table
c.execute('''CREATE TABLE "%s"
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              product_name text, txt text, img1 text,img2 text, img3 text)'''% x)
conn.commit()
conn.close()
