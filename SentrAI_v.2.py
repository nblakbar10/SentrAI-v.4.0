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
##emergency-nya
#!/usr/bin/python
import smbus
import math

#kodingan tombolnya
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

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
    send_data_api()

def send_data_api():
    tanggalnya = datetime.datetime.now()
    timestampStr = tanggalnya.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    ##kodingan buat send data ke Antares API
    antares.setDebug(True)
    antares.setAccessKey('3857828b743bc45b:43278715a207b29e')
    myData = {
        'Objek yang Dideteksi' : list_suara,
        'Tanggal & Waktu' : timestampStr,
        'Lokasi' : 'Samarinda, East Kalimantan, Indonesia (-0.502106, 117.153709)'
        }
    antares.send(myData, 'SentrAI', 'LocatedanSMSAPI')
    ######################################################
    msg = ("Objek yang Dideteksi : %s\tTanggal & Waktu : %s\t'Lokasi : Samarinda, East Kalimantan, Indonesia (-0.502106, 117.153709)'"% (list_suara,timestampStr))
    
    account_sid = "AC7caaf94ec4e2ae12a3e4c7304045fd6a"
    auth_token = "ef9f037b40713ce1a038b227dccab53f"

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to="+6282255443380",
        from_="+14844060521",
        body=msg
        )

class Emergency:
#def emergency(read_byte, read_word, read_word_2c, dist, get_y_rotation, get_z_rotation):
    # Register
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    
    #def __init__(self, read_byte, read_word, read_word_2c, dist, get_y_rotation, get_z_rotation):
     #   self.read_byte = read_byte
      #  self.read_word = read_word
       # self.read_word_2c = read_word_2c
        #self.dist = dist
      #  self.get_y_rotation = get_y_rotation
       # self.get_z_rotation = get_z_rotation
     
    def read_byte(reg):
        return bus.read_byte_data(address, reg)
    #return Emergency(read_byte)
     
    def read_word(reg):
        h = bus.read_byte_data(address, reg)
        l = bus.read_byte_data(address, reg+1)
        value = (h << 8) + l
        return value
    #return Emergency(read_word)
     
    def read_word_2c(reg):
        val = read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
    #return Emergency(read_word_2c)
     
    def dist(a,b):
        return math.sqrt((a*a)+(b*b))
    #return Emergency(dist)
     
    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)
    #return Emergency(get_y_rotation)

    def get_z_rotation(x,y,z):
        radians = math.atan2(z, dist(x,y))
        return math.degrees(radians)
    #return Emergency(get_z_rotation)
     
    bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
    address = 0x68       # via i2cdetect
     
    # Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)
     
    #return read_byte, read_work, read_word_2c, dist, get_y_rotation, get_z_rotation
    #return Emergency()
    
    while True :
        ##print "Accelerometer"

        percepatan_Xout = read_word_2c(0x3b)
        percepatan_Yout = read_word_2c(0x3d)
        percepatan_Zout = read_word_2c(0x3f)
         
        percepatan_Xout_skala = percepatan_Xout / 16384.0
        percepatan_Yout_skala = percepatan_Yout / 16384.0

        if (percepatan_Zout > 8000) or (percepatan_Yout > 8000) or (percepatan_Zout < -10000):
            print("PENGGUNA TERDETEKSI TERJATUH!!!")
            send_data_api()
        time.sleep(0.7)
    #return Emergency
    

    
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
    Emergency()
    
    ##emergency(read_byte, read_work, read_word_2c, dist, get_y_rotation, get_z_rotation)
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