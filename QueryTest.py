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

# c.execute('Delete From WeightPR') --- DELETE


conn.commit()
conn.close()

# get data:
# c.execute("Select date, EstimatedMax from WeightPR where Lift='Bench Press'")
# test = c.fetchall()
# for item in test:
#     print(item[0], item[1]) # get dates


# test insertion:
# item = [['Bench Press', '2021-3-2', 1, 1, 1], ['Bench Press', '2021-3-3', 2, 2, 2], ['Bench Press', '2021-3-4', 3, 3, 3], ['Bench Press', '2021-3-5', 4, 4, 4]]
# def data_entry(list_):
#     for item in list_:
#         c.execute("INSERT INTO WeightPR values (?, ?, ?, ?, ?)", item)
#     conn.commit()
# data_entry(item)