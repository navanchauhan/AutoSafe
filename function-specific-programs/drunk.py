from uber_rides.session import Session
from uber_rides.client import UberRidesClient


session = Session(server_token=<TOKEN>)
client = UberRidesClient(session)


print("Your Location Appears to be around places which sells \n alcohol, please taka the breathalyser test ")

bac = 0.02

if(bac >= 0.08):
	print("Please Do Not Drive!\n")
	print("I can call a cab if you want\n")
	print("Say No, to disagree, else I'll book the cab")
	input = yes
	if(input==no):
		print("You are not fit to drive")
		print("Text message to emergency contact sent")
		break
	print("Your cab has been booked, thank you for not driving")
	break
print("have a safe journey!")
	
