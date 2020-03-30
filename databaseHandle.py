import mysql.connector
mydb=mysql.connector.connect(
    host='us-cdbr-iron-east-01.cleardb.net',
    user='b1d1295e215409',
    password='0f7a8997',
    database='heroku_4b71b22231854d1'
)
restaurant=['Sepoy Grande','Radission Blu','Orchid','Gufha','Jalpaan Dining Saga','Kapoor cafe']
msg=1
# mysql://b1d1295e215409:0f7a8997@us-cdbr-iron-east-01.cleardb.net/heroku_4b71b22231854d1?reconnect=true

def showMenu(msg):
    mycursor = mydb.cursor()
    mycursor.execute("Select * from menu_" + restaurant[msg - 1].split()[0])
    menu = mycursor.fetchall()
    menustr = ""
    for i in range(len(menu)):
        menustr += menu[i][0] + " --->   ₹" + str(menu[i][1]) + "\n"
    return menustr
def showSeats(msg):
    mycursor = mydb.cursor()
    mycursor.execute("Select * from seat_" + restaurant[msg - 1].split()[0])
    seat = mycursor.fetchall()
    seatstr = "Time       Total available seats\n"
    for i in range(len(seat)):
        seatstr += str(seat[i][0]) + " PM  ---> " + str(seat[i][1]) + "\n"
    return seatstr

def bookSeat(msg):
    mycursor=mydb.cursor()

    restno=int(msg[0])-1
    time=msg.split()[0][2:]
    # cust_name=msg.split()[1:]
    mycursor.execute("Update seat_"+restaurant[restno].split()[0]+" set avail_table = avail_table -1 where time ="+time)
    mydb.commit()
    insert(msg)
    return 1
def insert(msg):
    mycursor1 = mydb.cursor()
    restno = int(msg[0]) - 1
    time = msg.split()[0][2:]
    # cust_name = msg.split()[1:]
    cust_name = ""
    for i in range(1, len(msg.split())):
        cust_name += msg.split()[i] + " "
    insertFn = "Insert into bookings_" + restaurant[restno].split()[0] + " (cust_name, time) Values (%s, %s)"
    bookingDetails = (cust_name, time)
    mycursor1.execute(insertFn,bookingDetails)
    mydb.commit()

