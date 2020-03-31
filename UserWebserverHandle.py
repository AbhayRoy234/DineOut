#author:AMIT
#this is the flask application that fetch data from twilio api and gives response on basis of the instructions recieved

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import databaseHandle

app = Flask(__name__)
restaurant = ['Sepoy Grande', 'Radission Blu', 'Orchid', 'Gufha', 'Jalpaan Dining Saga', 'Kapoor\'s cafe']


@app.route("/")
def hello():
    return "User Webserver"


@app.route("/user", methods=['POST'])
def user_sms_reply():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    if msg == 'Dine out':
        resp.message(
            "Here we have a list of restaurants from which u can pick any to have a delightful experience.\nSelect the option accordingly\n1. Sepoy Grande\n2. Radission Blu\n3. Orchid\n4. Gufha\n5. Jalpaan Dining Saga\n6. Kapoor's cafe")
    elif msg.isdigit() and int(msg) < 7:
        menu = databaseHandle.showMenu(int(msg))
        seats = databaseHandle.showSeats(int(msg))
        resp.message(
            "Menu: \n" + menu + "\n" + seats + "\nTo book a table for this resturant please specify the timing along with the resturant no. followed by your name \nFor instance if you have to select \n" + str(
                msg) + ". " + restaurant[int(msg) - 1] + " for 10 o'clock give instruction as:\n" + str(
                msg) + ".10  Your name")
    elif len(msg) >= 5 and msg[1] == '.' and int(msg[0]) < 7 and int(msg.split()[0][2:]) < 13:
        book = 0
        book = databaseHandle.bookSeat(msg)
        cust_name = ""
        for i in range(1, len(msg.split())):
            cust_name += msg.split()[i] + " "
        if book == 1:
            resp.message("Congratulation, " + cust_name + "!\nYour booking for " + restaurant[
                int(msg[0]) - 1] + " has been successfully made for " + msg.split()[0][
                                                                        2:] + " pm.\nThanks for using our service")
        else:
            resp.message(
                "We were unable to process your request at the moment, May be all the tables have been booked for the resturant you are tring for\nPlease try booking table in a different restaurant\nHoping to serve you soon!")
    else:
        resp.message("Invaild Request!\nPlease try giving\n'Dine out'")
    return str(resp)


@app.route("/hotel", methods=['GET', 'POST'])
def hotel_sms_reply():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    if msg == 'Dine out':
        resp.message(
            "Greeting you on our platform!\nYou can manage your restaurant's data\nPartner resturants are:\n1. Sepoy Grande\n2. Radission Blu\n3. Orchid\n4. Gufha\n5. Jalpaan Dining Saga\n6. Kapoor's cafe\n\nTasks that can be performed:\na. View Bookings\nb. Update seat \nc. Add to Menu\nSelect the task to be performed by giving a,b or c as instruction")
    elif msg == 'a':
        view_booking_msg = "To view bookings of your restaurant\nGive instruction as:\n hotel no. bookings <password>\nfor instance if you want to view bookings of Sepoy Grande give this instruction\n1 bookings ****"
        resp.message(view_booking_msg)
    elif msg == 'b':
        update_seat_msg = "To update available tables for your restaurant\nGive instruction as:\n hotel no. table <time> <no. of tables> <password>\nfor instance if you want to update no. of available tables for Sepoy Grande give this instruction\n1 table 3 60 ****"
        resp.message(update_seat_msg)
    elif msg == 'c':
        append_menu_msg="To update menu of your restaurant\nGive instruction as:\n hotel no. menu <name of the item> <price> <password>\nfor instance if you want to update menu of Sepoy Grande give this instruction\n1 menu roti 30 ****"
        resp.message(append_menu_msg)
    elif len(msg)>10 and len(msg.split())>2 and int(msg.split()[0])<7:
        if msg.split()[1] == 'bookings':
            showBooking,success=databaseHandle.showBookings(msg)
            if success:
                resp.message(showBooking)
            else :
                error_msg="Either the instruction is invalid or password\nPlease try again"
                resp.message(error_msg)
        elif msg.split()[1] == 'table':
            seatstr,success=databaseHandle.updateSeats(msg)
            if success:
                resp.message("No. of available tables have been successfully updated for "+restaurant[int(msg[0])-1]+"\n"+seatstr)
            else :
                error_msg="Either the instruction or password is invalid\nPlease try again !"
                resp.message(error_msg)
        elif msg.split()[1] == 'menu':
            menuStr,success = databaseHandle.updateMenu(msg,len)
            if success:
                resp.message("Menu have been successfully updated for "+restaurant[int(msg[0])-1]+"\n"+menuStr)
            else:
                error_msg = "Either the instruction is invalid or password\nPlease try again"
                resp.message(error_msg)
        else:
            error_msg = "Invalid instruction!\nTry giving 'Dine out'"
            resp.message(error_msg)
    else:
        error_msg = "Invalid instruction!\nTry giving 'Dine out'"
        resp.message(error_msg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
