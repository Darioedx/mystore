import sqlite3
db_local = 'database.db'

conn = sqlite3.connect(db_local)
c = conn.cursor()

# populate

c.execute('''INSERT INTO category ( cat_name, txt,img)
          VALUES ("Cat1","breve descripcion","static/img_1.jpg")''')

conn.commit()
conn.close()
