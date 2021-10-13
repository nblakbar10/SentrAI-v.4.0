# USAGE
# python openvino_real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from pydub import AudioSegment
from pydub.playback import play
from antares_http import antares
from twilio.rest import Client
import requests
import numpy as np
import argparse
import imutils
import time
import cv2
import gtts
import RPi.GPIO as GPIO
import datetime
from firebase import firebase

#kodingan tombolnya
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

#send data to firebase
firebaseURL = 'https://sentrai.firebaseio.com/'

firebase = firebase.FirebaseApplication(firebaseURL, None)

#bikin fungsi def buat manggil dan mengaktifkan speechnya
def putarsuara(list_suara):
    play(AudioSegment.from_mp3("didepanada.mp3"))
    for objeknya in list_suara:
        if (objeknya == "orang"):
            play(AudioSegment.from_mp3("orang.mp3"))
        elif (objeknya == "botol"):
            play(AudioSegment.from_mp3("botol.mp3"))
        elif (objeknya == "kursi"):
            play(AudioSegment.from_mp3("kursi.mp3"))
        elif (objeknya == "kucing"):
            play(AudioSegment.from_mp3("kucing.mp3"))
        elif (objeknya == "motor") :
            play(AudioSegment.from_mp3("motor.mp3"))
        elif (objeknya == "mobil") :
            play(AudioSegment.from_mp3("mobil.mp3"))
        elif (objeknya == "anjing"):
            play(AudioSegment.from_mp3("anjing.mp3"))
        elif (objeknya == "kursi") :
            play(AudioSegment.from_mp3("kursi.mp3"))
        elif (objeknya == "sepeda") :
            play(AudioSegment.from_mp3("sepeda.mp3"))
        elif (objeknya == "tv") :
            play(AudioSegment.from_mp3("tv.mp3"))
        elif (objeknya == "bis") :
            play(AudioSegment.from_mp3("bis.mp3"))
        elif (objeknya == "meja") :
            play(AudioSegment.from_mp3("meja.mp3"))
            
    ###kodenya buat API
    tanggalnya = datetime.datetime.now()
    timestampStr = tanggalnya.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    ##kodingan buat send data ke Antares API
    antares.setDebug(True)
    antares.setAccessKey('3857828b743bc45b:43278715a207b29e')
    myData = {
        'Objek terakhir yang Dideteksi' : list_suara,
        'Tanggal & Waktu' : timestampStr,
        'Lokasi' : 'Samarinda, East Kalimantan, Indonesia (-0.502106, 117.153709)'
        }
    antares.send(myData, 'SentrAI', 'LocatedanSMSAPI')
    ######################################################
    msg = ("Objek yang Dideteksi : %s\tTanggal & Waktu : %s\t'Lokasi : Samarinda, East Kalimantan, Indonesia (-0.502106, 117.153709)'"% (list_suara,timestampStr))
    
    account_sid = "AC11931cc006dd02b4f61899cd57a0b06b"
    auth_token = "f5e2338f5ae90c1788ac719b6fef8618"

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to="+6282255443380",
        from_="+16503895744",
        body=msg
        )
    
    try:
        data = {"timestamp":timestampStr,"Objek terakhir yang Dideteksi" : list_suara, "lat": -0.502106, "lon": 117.153709}
        firebase.post('/location', data)

    except Exception as e:
        print("Can't update Firebase with exception:"+str(e) )
    ###print("SMS Emergency Terkirim!")
        
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
ap.add_argument("-u", "--movidius", type=bool, default=0,
	help="boolean indicating if the Movidius should be used")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "sepeda", "bird", "boat",
	"botol", "bis", "mobil", "kucing", "kursi", "cow", "meja",
	"anjing", "horse", "motor", "orang", "pottedplant", "sheep",
	"sofa", "train", "tv"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# specify the target device as the Myriad processor on the NCS
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
#VideoStream.rotation = 90
time.sleep(1.0)
fps = FPS().start()
#engine = pyttsx3.init();

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = imutils.rotate(frame, 90) ##ini buat balikin gambarnya

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (180, 180), 127.5) ##sebelumnya 300.300

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    list_suara = []
    for i in np.arange(0, detections.shape[2]):
        obyek = ""
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            obyek = CLASSES[idx]
        if obyek not in list_suara and obyek != "":
            list_suara.append(obyek)
    
    
                    
    if GPIO.input(10) == GPIO.HIGH:
        putarsuara(list_suara)
        ##print(list_suara)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    ###exec(open("gyroscope.py").read())
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()