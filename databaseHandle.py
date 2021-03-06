#this file handles all the request from WebserverHandle

import mysql.connector
def connect():
    try:
        mydb = mysql.connector.connect(
            host='us-cdbr-iron-east-01.cleardb.net',
            user='b1d1295e215409',
            password='0f7a8997',
            database='heroku_4b71b22231854d1'
        )
    except:
        connect()
    return mydb


restaurant=['Sepoy Grande','Radission Blu','Orchid','Gufha','Jalpaan Dining Saga','Kapoor cafe']
passwords={1:'0001',2:'0002',3:'0003',4:'0004',5:'0005',6:'0006'}
# mysql://b1d1295e215409:0f7a8997@us-cdbr-iron-east-01.cleardb.net/heroku_4b71b22231854d1?reconnect=true
def showMenu(msg):
    mydb=connect()
    mycursor = mydb.cursor()
    mycursor.execute("Select * from menu_" + restaurant[msg - 1].split()[0])
    menu = mycursor.fetchall()
    menustr = ""
    for i in range(len(menu)):
        menustr += menu[i][0] + " --->   ₹" + str(menu[i][1]) + "\n"
    return menustr
def showSeats(msg):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("Select * from seat_" + restaurant[msg - 1].split()[0])
    seat = mycursor.fetchall()
    seatstr = "Time       Total available seats\n"
    for i in range(len(seat)):
        seatstr += str(seat[i][0]) + " PM  ---> " + str(seat[i][1]) + "\n"
    return seatstr

def bookSeat(msg):
    mydb = connect()
    mycursor=mydb.cursor()
    restno=int(msg[0])-1
    time=msg.split()[0][2:]
    mycursor.execute("Update seat_"+restaurant[restno].split()[0]+" set avail_table = avail_table -1 where time ="+time)
    mycursor.execute("Select avail_table from seat_"+restaurant[restno].split()[0]+" where time ="+time)
    avail_seat = mycursor.fetchall()
    if int(avail_seat[0][0])>0:
        mydb.commit()
        insert(msg)
        return 1
    else:
        return 0
def insert(msg):
    mydb = connect()
    mycursor1 = mydb.cursor()
    restno = int(msg[0]) - 1
    time = msg.split()[0][2:]
    # cust_name = msg.split()[1:]
    cust_name = ""
    for i in range(1, len(msg.split())):
        cust_name += msg.split()[i] + " "
    insertFn = "Insert into bookings_" + restaurant[restno].split()[0] + " (cust_name, time) Values (%s, %s)"
    bookingDetails = (cust_name, time)
    mycursor1.execute(insertFn, bookingDetails)
    mydb.commit()
def showBookings(msg):
    restno=int(msg[0])-1
    paswd=msg.split()[2]
    if passwords[restno+1] == paswd:
        mydb = connect()
        mycursor = mydb.cursor()
        try:
            mycursor.execute("Select * from bookings_" + restaurant[restno].split()[0])
            bookings = mycursor.fetchall()
            bookstr = "Time            Customer Name\n"
            for i in range(len(bookings)):
                bookstr += str(bookings[i][1]) + " PM   ===>  " + str(bookings[i][0]) + "\n"
            return bookstr,1
        except:
            return " ",0
    else:
        return " ",0
def updateSeats(msg):
    restno = int(msg[0]) - 1
    paswd = msg.split()[4]
    updatedSeats=msg.split()[3]
    if passwords[restno + 1] == paswd and int(updatedSeats)>=0:
        time=msg.split()[2]
        mydb = connect()
        mycursor = mydb.cursor()
        try:
            mycursor.execute(
                "Update seat_" + restaurant[restno].split()[0] + " set avail_table = "+updatedSeats + " where time =" + time)
            mydb.commit()
            seatstr=showSeats(restno+1)
            return seatstr, 1
        except:
            return " ",0
    else:
        return " ", 0
def updateMenu(msg):
    lent=len(msg.split())
    restno = int(msg[0]) - 1
    paswd = msg.split()[lent-1]
    if passwords[restno + 1] == paswd:
        price=msg.split()[lent-2]
        dish=""
        for i in (2,lent-3):
            dish+=msg.split()[i]+" "
        mydb = connect()
        mycursor = mydb.cursor()
        try:
            insertFn="INSERT into menu_"+restaurant[restno].split()[0] +" (dish, price) Values (%s, %s)"
            menu=(dish,price)
            mycursor.execute(insertFn,menu)
            mydb.commit()
            menuStr = showMenu(restno + 1)
            return menuStr, 1
        except:
            return " ",0
    else:
        return " ", 0