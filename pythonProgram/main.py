"""AutoSafe
Modular Road-Safety Toolkit

"""
#pylint: disable=C0103,C0111
import argparse
import datetime
import time
import overpy
import simplejson as sjson
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
#import playsound
import imutils
import dlib
import cv2
#from uber_rides.session import Session
#from uber_rides.client import UberRidesClient
import tweepy
import requests

#import geocoder
#import obd

######################
# Defining Variables #
######################

radius = str(100) # Radius for maxspeed function. taken as a string because gets concatenated

################
# Dummy Values #
################


#Latitude
glat = 28.544565 #28.546519
#Longitude
glng = 77.193320 #77.179248

# Commented this as we are not on a road I guess?

#g = geocoder.ip('me')
#print(g.latlng)

#####################
#  Real Time Values #
#####################

#glat = g.lat
#glng = g.lng

###################
# Dummy OBD Setup #
###################

##############################################################
# What the commands are doing:                               #
# It setups and asynchronous watch over the speed of the car #
# this means that the speed's data is constantly updated     #
# This makes the while loop work                             #
##############################################################


#connection = obd.Async() # auto-connects to USB or RF port
#connection.watch(obd.commands.SPEED) # select an OBD command (sensor)
#connections.start()
#carSpeed = connection.query(obd.commands.SPEED) # send the command, and parse the response

#carSpeed = 30

#####################
# Tweeting Function #
#####################

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def tweetMe():
    cfg = {
        "consumer_key":"knQFpTnjuSvr6OxYwebt3wyrd",
        "consumer_secret":"Mhex3oRkmaF7lD3hoMvHpAD6ctW0ugKYCopTlhc0JzOLOMIZ0w",
        "access_token":"2846631344-wEozinvHfEIFxFVy51I6te8SrN5OTFtU00wxsiz",
        "access_token_secret":"Nfx1U8a2TjAQXFLBrJIyy2p36sjBGAWFIthLc1cIoI56U"
    }

    api = get_api(cfg)
    headers = {
        'Accept': 'application/json',
        'user-key': 'a530c1424d9abe5442fa22f77ce03d25',
                }

    params = (
        ('lat', '28.546519'),
        ('lon', '77.179248'),
    )
    url = 'https://developers.zomato.com/api/v2.1/geocode'
    response = requests.get(url, headers=headers, params=params)
    loc = response.json()['location']['title']
    now = datetime.datetime.now()
    now = str(now)
    tweetMsg = "Stay Alert! Sudden braking at: ", loc, "on", now
    api.update_status(status=tweetMsg)
    #print(status)
    print(tweetMsg)
    exit

################################
# Fetching Details from Zomato #
################################

def getRes():
    res = []
    headers = {
        'Accept': 'application/json',
        'user-key': 'a530c1424d9abe5442fa22f77ce03d25',
    }

    params = (
        ('lat', '28.546519'),
        ('lon', '77.179248'),
    )
    url = 'https://developers.zomato.com/api/v2.1/geocode'
    response = requests.get(url, headers=headers, params=params)
    res = response.json()['popularity']['nearby_res']
    return res

def getDetails(res):
    headers = {
        'Accept': 'application/json',
        'user-key': 'a530c1424d9abe5442fa22f77ce03d25',
    }
    url = "https://developers.zomato.com/api/v2.1/restaurant?res_id=" + str(res[0])
    newResponse = requests.get(url, headers=headers)
    #newRes = []
    resName = newResponse.json()['name']
    resAddress = newResponse.json()['location']['address']
    print("You are feeling sleepy, why don't you take a break?\n")
    print("Your nearest eatery is " + resName, "\n")
    print(resName + " is at " + resAddress, "\n")

def zomato():
    res = getRes()
    getDetails(res)

############################
# Combatting Drunk Driving #
############################

def drunk():
    print("Your appear to be around places which sell \n alcohol, take the breathalyser test")

    bac_raw = str(open("./files/bac.txt", "r").read())
    bac = float(float(bac_raw)/100)
    print(bac)
    if bac >= 0.08:
        print("Please Do Not Drive!\n")
        print("I can call a cab if you want\n")
        print("")
        answer = input("Say No, to disagree, else I'll book the cab: \n")
        if answer == "no":
            print("You are not fit to drive")
            print("Text message to emergency contact sent")
        print("Your cab has been booked, thank you for not driving")
    print("have a safe journey!")


def sound_alarm():
    print('You Sleep You Lose')

def eye_aspect_ratio(eye):

    # Computes the euclidean distances between the two sets of eyes
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear

shape_predictor = "./files/shape_predictor_68_face_landmarks.dat"


EYE_AR_THRESH = 0.2 # If the EAR goes < this for 48 frames, it is counted as drowsiness
EYE_AR_CONSEC_FRAMES = 24




########################
# Drowsiness Detection #
########################

def sleepiness():

    COUNTER = 0
    #ALERT = False

    print("Initialising Facial Landmark Predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    print("Starting Video Stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < EYE_AR_THRESH:
                COUNTER += 1

                # if the eyes were closed for a sufficient number of
                # then sound the alarm
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    # if the alarm is not on, turn it on
                    if not ALARM_ON:
                        ALARM_ON = True

                    # draw an alarm on the frame
                    cv2.putText(frame, "Sleepiness Detected!", (10, 30),
                    	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    print("Sleepiness Detected!")
                    print("\n \n \n")
                    zomato()
                    time.sleep(5)
                    exit()



            else:
                COUNTER = 0
                ALARM_ON = False

            cv2.putText(frame, "Ratio: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # breaks loop on q
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()

##############################
# Speed Limit Fetch Function #
##############################

def maxspeed(coordinates, radius):

    lat, lon = coordinates
    api = overpy.Overpass()

    #######################
    # Query for Open Maps #
    #######################

    result = api.query("""
            way(around:""" + radius + """,""" + lat  + """,""" + lon  + """) ["maxspeed"];
                (._;>;);
                    out body;
                        """)

    results_list = []
    for way in result.ways:
        road = {}
        road["name"] = way.tags.get("name", "n/a")
        road["speed_limit"] = way.tags.get("maxspeed", "n/a")
        nodes = []
        for node in way.nodes:
            nodes.append((node.lat, node.lon))
        road["nodes"] = nodes
        results_list.append(road)
        return results_list




#########################################################################
# Gives data to the function and gets json in return. 					#
#This json is then parsed. Then the double quotes are stripped off it 	#
#########################################################################
def speedlim():
    speedLimit = sjson.dumps(maxspeed((str(glat), str(glng)), radius)[0]['speed_limit']).strip('\"')
    while True:
        carSpeedDummy = open("./files/carSpeed.txt", "r")
        carSpeed = carSpeedDummy.read()
        #print(carSpeed)
        #carSpeed = 29
        while int(carSpeed) > int(speedLimit):
            carSpeedDummy = open("./files/carSpeed.txt", "r")
            carSpeed = carSpeedDummy.read()
            print("Over The Speed Limit")
            time.sleep(5)
        while int(carSpeed) <= int(speedLimit):
            carSpeedDummy = open("./files/carSpeed.txt", "r")
            carSpeed = carSpeedDummy.read()
            print("Under the Speed Limit with a speed of ", carSpeed)
            time.sleep(5)

##################
# Sudden Braking #
##################

def brakes():
    while True:
        tweetMe()

#####################################################
# Using Argument Parse to run one command at a time #
#####################################################

parser = argparse.ArgumentParser()
FUNCTION_MAP = {'overspeed' : speedlim, 'sleep-detector' : sleepiness,
                'sudden-braking' : brakes, 'drunk' : drunk}
parser.add_argument('function', choices=list(FUNCTION_MAP))
args = parser.parse_args()
FUNC = FUNCTION_MAP[args.function]
FUNC()
