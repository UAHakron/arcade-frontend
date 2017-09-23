#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import requests
import json
from Tkinter import *

continue_reading = True




#function
def scanTag():
    #scan tag
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # Welcome message
    print "Welcome to Kyle's NFC Arcade data read example"
    print "Press Ctrl-C to stop."


    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
    
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
    
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

       # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print "Card read UID: "+str(hex(uid[0]))+"."+str(hex(uid[1]))+"."+str(hex(uid[2]))+"."+str(hex(uid[3]))
            
            #API stuff
            
            #get request on email
            email_exists = requests.get('https://hakron.io/arcade/people/'+str(email_text.get()))
            
                #if email exists
            if email_exists.status_code == 200:
                user_data = json.loads(email_exists.json())
                update_id = requests.post("https:/hakron.io/arcade/tags/" + str(hex(uid[0]))+"."+str(hex(uid[1]))+"."+str(hex(uid[2]))+"."+str(hex(uid[3])) + "/people", json={"_id":user_data["_id"]})
                #if email does not exist
            else:
                create_user = requests.post("https://hakron.io/arcade/people", json={"name":str(name_text.get()),"nfc":str(hex(uid[0]))+"."+str(hex(uid[1]))+"."+str(hex(uid[2]))+"."+str(hex(uid[3])),"email":str(email_text.get()) ,"bits":"0"})
                user_data = json.loads(create_user.json())
                update_id = requests.post("https:/hakron.io/arcade/tags/" + str(hex(uid[0]))+"."+str(hex(uid[1]))+"."+str(hex(uid[2]))+"."+str(hex(uid[3])) + "/people", json={"_id":user_data["_id"]})
                
            #


            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

           # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print "Authentication error"
            break


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)


#create window
window=Tk()

#define Labels
l1=Label(window, text="Name:")
l1.config(font=("Comic Sans", 44))
l1.grid(row=0,column=0,sticky=E)

l2=Label(window, text="Email:")
l2.config(font=("Comic Sans", 44))
l2.grid(row=1,column=0,sticky=E)

# define Entries
name_text=StringVar()
e1=Entry(window,textvariable=name_text)
e1.grid(row=0,column=1)

email_text=StringVar()
e2=Entry(window,textvariable=email_text)
e2.grid(row=1,column=1)

#define buttons
b1=Button(window,text="Submit and Scan", width=32,height=6, command=scanTag)
b1.grid( columnspan=2)

window.mainloop()
