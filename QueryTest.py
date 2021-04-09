import sqlite3
# C:\Users\david\PycharmProjects\Weight.db
# cursor.execute('''Create Table IF NOT EXISTS WeightPR (
#                 Lift BLOB,
#                 Date BLOB,
#                 InputWeight REAL,
#                 Rep REAL,
#                 EstimatedMax REAL
#                 )''')

conn = sqlite3.connect('Weight.db')
c = conn.cursor()
#c.execute("Insert into WeightPR Values ('3','3','3','3','3')")
c.execute("Select * from WeightPR")
print(c.fetchall())
conn.commit()
conn.close()
