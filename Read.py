#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import smtplib
import time
import requests

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

continue_reading = True

def sendMail(kartID,tf):
    fromaddr = "rasptestmail1@gmail.com"
    toaddr = "bervandaslik@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    
    #Servisten dönen değere göre valid ya da invalid seçimi
    if tf!='False':
        msg['Subject'] = "RFID Kayıtlı Giriş."
        body = "Kaydedilmiş RFID Kart UID : "+kartID
        msg.attach(MIMEText(body, 'plain'))
    else:
        msg['Subject'] = "RFID Bilinmeyen Kart"
        body = "Bilinmeyen RFID Kart UID :"+kartID
        msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "bervan123+")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Uygulamadan çıkarken GPIO pinlerini boşalt
def end_read(signal,frame):
    global continue_reading
    print "Uygulama Durduruldu."
    continue_reading = False
    GPIO.cleanup()

# Kesme
signal.signal(signal.SIGINT, end_read)

# MFRC522 nesne türetme
MIFAREReader = MFRC522.MFRC522()

# Karşılama Ekranı
print "RC522 RFID Kart Okuma"
print "Ctrl-C ile Uygulamayı Durdur."

# Okuma baslar ve durdurulana kadar devam eder
while continue_reading:
    
    # kart tarama   
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Eğer kart bulunursa
    if status == MIFAREReader.MI_OK:
        print "Kart Okundu"
    
    # Kartın UID si okunur.
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # Kartın uid si varsa devam et
    if status == MIFAREReader.MI_OK:
        kuid=str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        # UID yazdır.
        print "Kart UID: "+kuid
        
        # Servisten kartın uid si ile istekte bulunma
        tf=requests.get("http://localhost:5000/"+kuid)
        
        print tf.text
        
        #Gelen cevaba(True or False) göre mail gönder
        sendMail(kuid,tf.text)
        time.sleep(2)
            
        
        
        MIFAREReader.MFRC522_SelectTag(uid)



