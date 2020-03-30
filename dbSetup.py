import mysql.connector
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='amit',
    database='restaurants'
)
restaurant=['Sepoy Grande','Radission Blu','Orchid','Gufha','Jalpaan Dining Saga','Kapoor cafe']
mycursor = mydb.cursor()
# print(restaurant[0].split()[0])
insertFn="Insert into seat_"+restaurant[4].split()[0]+" (time, avail_table) Values (%s, %s)"
dropFn="Drop Table seat_"+restaurant[5].split('\'')[0]
createFn = "Create Table bookings_" + restaurant[5].split()[0] + " (cust_name VARCHAR(100),time INT(2))"
menu=[(12,35),
      (1,35),
      (2,35),
      (3,35),
      (4,35),
      (5,35),
      (6,35),
      (7,35),
      (8,35),
      (9,35),
      (10,35),
      (11,35)]
# mycursor.executemany(insertFn,menu)
mycursor.execute(createFn)
mydb.commit()
