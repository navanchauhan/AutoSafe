import requests
import simplejson as sjson
import json

res = []

def getRes():
	headers = {
	    'Accept': 'application/json',
	    'user-key': 'a530c1424d9abe5442fa22f77ce03d25',
	}

	params = (
	    ('lat', '28.546519'),
	    ('lon', '77.179248'),
	)

	response = requests.get('https://developers.zomato.com/api/v2.1/geocode', headers=headers, params=params)
	res = response.json()['popularity']['nearby_res']
	return res

def getDetails(res):
	headers = {
	    'Accept': 'application/json',
	    'user-key': 'a530c1424d9abe5442fa22f77ce03d25',
	}
	url = "https://developers.zomato.com/api/v2.1/restaurant?res_id=" + str(res[0])
	newResponse = requests.get(url, headers=headers)
	newRes = []
	resName = newResponse.json()['name']
	resAddress = newResponse.json()['location']['address']
	print("You are feeling sleepy, why don't you take a break?\n")
	print("Your nearest eatery is " + resName,"\n")
	print(resName + " is at " + resAddress,"\n")
def zomato():

	res = getRes()
	getDetails(res)
zomato()


