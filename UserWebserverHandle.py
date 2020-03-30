from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import databaseHandle
app = Flask(__name__)
resturant=['Sepoy Grande','Radission Blu','Orchid','Gufha','Jalpaan Dining Saga','Kapoor\'s cafe']
@app.route("/")
def hello():
    return "User Webserver"
@app.route("/user", methods=['POST'])
def user_sms_reply():
    msg=request.form.get('Body')
    resp = MessagingResponse()
    if msg=='Dine out':
        resp.message("Here we have a list of restaurants from which u can pick any to have a delightful experience.\nSelect the option accordingly\n1. Sepoy Grande\n2. Radission Blu\n3. Orchid\n4. Gufha\n5. Jalpaan Dining Saga\n6. Kapoor's cafe")
    elif msg.isdigit() and int(msg)<7:
        menu=databaseHandle.showMenu(int(msg))
        seats=databaseHandle.showSeats(int(msg))
        resp.message("Menu: \n"+menu+"\n"+seats+"\nTo select seats for this resturant please specify the timing along with the resturant no. followed by your name \nFor instance if you have to select \n"+str(msg)+". "+resturant[int(msg)-1]+" for 10 o'clock give instruction as:\n"+str(msg)+".10  Your name")
    elif len(msg)>= 5 and msg[1]=='.' and int(msg[0])<7 and int(msg.split()[0][2:])<13:
        book=0
        book=databaseHandle.bookSeat(msg)
        cust_name=""
        for i in range(1,len(msg.split())):
            cust_name+=msg.split()[i]+" "
        if book==1:
            resp.message("Congratulation, "+cust_name+"!\nYour booking for "+resturant[int(msg[0])-1]+" has been successfully made for "+msg.split()[0][2:]+" pm.\nThanks for using our service")
        else:
            resp.message("We were unable to process your request at the moment, May be all the seats have been booked for the resturant you are tring for\nPlease try booking seats in a different resturant\nHoping to serve you soon!")
    else:
        resp.message("Invaild Request!\nPlease try giving\n'Dine out'")
    return str(resp)
@app.route("/hotelMGR", methods=['POST'])
def hotelMGR_sms_reply():
    msg=request.form.get('Body')
    resp = MessagingResponse()
    if msg=='Dine out':
        resp.message("Tell us ab")
    if msg[:4]=='Admin':
        databaseHandle.admin(msg)
    else:
        resp.message("Invaild Request!\nPlease try giving\n'Dine Out'")
    return str(resp)
if __name__ == "__main__":
    app.run(debug=True)