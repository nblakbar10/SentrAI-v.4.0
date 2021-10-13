#!/usr/bin/python
import smbus
import math
import time
import datetime
from antares_http import antares
from twilio.rest import Client
# Register

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z, dist(x,y))
    return math.degrees(radians)
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
bus.write_byte_data(address, power_mgmt_1, 0)
 
while True :
    
    percepatan_yout = read_word_2c(0x3d)
    percepatan_zout = read_word_2c(0x3f)

    percepatan_yout_skala = percepatan_yout / 16384.0
    percepatan_zout_skala = percepatan_zout / 16384.0

    if (percepatan_zout > 8000) or (percepatan_yout > 8000) or (percepatan_zout < -10000):
        hasil = "PENGGUNA TERDETEKSI TERJATUH!!!"
        if hasil == ("PENGGUNA TERDETEKSI TERJATUH!!!"):
            print (hasil)
            tanggalnya = datetime.datetime.now()
            timestampStr = tanggalnya.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            ##kodingan buat send data ke Antares API
            antares.setDebug(True)
            antares.setAccessKey('3857828b743bc45b:43278715a207b29e')
            myData = {
                ##'Objek yang Dideteksi' : list_suara,
                'Tanggal & Waktu INSIDEN' : timestampStr,
                'Lokasi INSIDEN' : 'Samarinda, East Kalimantan, Indonesia (-0.502106, 117.153709)'
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
            
            ###print("SMS Emergency Terkirim!")
            
    time.sleep(1)
    ##time.sleep(7)
