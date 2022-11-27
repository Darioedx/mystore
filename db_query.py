import sqlite3

db_local = 'database.db'
x = 24
y ="productName2"
conn = sqlite3.connect(db_local)
c = conn.cursor()
#c.execute('''SELECT qty FROM "%s" WHERE product_name == (?)'''% x, ( y,))
#category_data = c.fetchall()
c.execute('''SELECT * FROM "%s" WHERE  product_name  IN (?)'''% x, ( y,))
category_data = c.fetchall()
for categorys in category_data:
    print(categorys)
conn.commit()
conn.close()