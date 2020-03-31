#author:AMIT
#this python file was used to create the database at the local host futher the database was hosted on the heroku along with the flask application

import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='amit',
    database='restaurants'
)
restaurant = ['Sepoy Grande', 'Radission Blu', 'Orchid', 'Gufha', 'Jalpaan Dining Saga', 'Kapoor cafe']
mycursor = mydb.cursor()
# print(restaurant[0].split()[0])
insertFn = "Insert into seat_" + restaurant[4].split()[0] + " (time, avail_table) Values (%s, %s)"
dropFn = "Drop Table seat_" + restaurant[5].split('\'')[0]
createFn = "Create Table bookings_" + restaurant[5].split()[0] + " (cust_name VARCHAR(100),time INT(2))"
menu = [(12, 35),
        (1, 35),
        (2, 35),
        (3, 35),
        (4, 35),
        (5, 35),
        (6, 35),
        (7, 35),
        (8, 35),
        (9, 35),
        (10, 35),
        (11, 35)]
# mycursor.executemany(insertFn,menu)
# mycursor.execute(createFn)
# mydb.commit()
passwords={1:'0001',2:'0002',3:'0003',4:'0004',5:'0005',6:'0006'}
msg="1 menu tandoori roti 30 0001"
list=msg.split()
str=""
for i in (2,len(list)-3):
    str+=list[i]+" "
    print(i)
print(str[:])
