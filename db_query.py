import sqlite3
db_local = 'database.db'

conn = sqlite3.connect(db_local)
c = conn.cursor()


c.execute('''SELECT * FROM productos WHERE category = "Cat1"
''')
category_data = c.fetchall()
for categorys in category_data:
    print(categorys)
conn.commit()
conn.close()