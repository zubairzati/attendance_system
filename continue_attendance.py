from tkinter import *
# import cv2
# import numpy as np
import face_recognition
import os
from datetime import datetime
import pyttsx3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
# import datetime
import time

path = 'imagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

root = Tk()

# root window title and dimension
root.title("Welcome to DIEMS,Aurangabad")
root.geometry('1280x720')
root.resizable(True, False)
root.configure(bg='#40E0D0')

canvas_width = 350
canvas_height = 150

canvas = Canvas(root,
                width=400,
                height=170)
canvas.place(x=510,
             y=60)

imglogo = PhotoImage(file="logo.png")
canvas.create_image(20, 20, anchor=NW, image=imglogo)

global key
key = ''

ts = time.time()
date = datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }

# adding a label to the root window
lbl = tk.Label(root, text="DIEMS Attendance System", fg="#4863A0", bg="#40E0D0")
lbl.place(x=305,
          y=10)
lbl.configure(font=("Georgia", 40, "bold"))

lbl2 = Label(root, text="E&Tc Department", fg="#4863A0", bg="#40E0D0")
lbl2.place(x=450,
           y=280)
lbl2.configure(font=("Georgia", 40, "bold"))

lbl3 = Label(root, text="Ready", bg="#40E0D0")
lbl3.place(x=590,
           y=430)
lbl3.configure(font=("Georgia", 40, "bold"))

Attendance= "Attendance_" + date + ".csv"
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


def onStart():
    print('starting')


def onWord(name, location, length):
    print('word', name, location, length)


def onEnd(name, completed):
    print('finishing', name, completed)


engine = pyttsx3.init()

engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):

    with open(Attendance, 'a+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{"In Time " + dtString}')


def markAttendanceex(name):
    with open(Attendance, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name in nameList:
            now2 = datetime.now()
            dtString2 = now2.strftime('%H:%M:%S')
            indexq=nameList.index(name)
            print(indexq)
            print(myDataList)
            #print(nameList)
            if name in nameList:
                f.writelines(f'\n{name},{"  Out Time " + dtString2}')


######################################################

######################################################




encodeListKnown = findEncodings(images)
print('Encoding complete')


# function to display text when
# button is clicked


def clicked():
    lbl3.configure(text="Entry Attendance Marked ", fg="Green")
    lbl3.place(x=320,
               y=480)
    # vid = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture(0)

    vid = cv2.VideoCapture(0)
    while True:
            # Capture the video frame

            # by frame
            # ret, frame = vid.read()

            # Display the resulting frame
            # cv2.imshow('frame', frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            #success, img = vid.read()
            ret, img = vid.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img,
                                #"Hershey Complex : ",
                                name,
                                (20, 160),
                                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                                fontScale=1,
                                color=(255, 255, 255))
                    l = name
                    engine.say('wellcome ' + l + 'to Electronics Department Have A Nice Day')
                    # engine.say(l)
                    engine.runAndWait()
                    # cv2.putText(img,name(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                    markAttendance(name)
                    # vid.release()

            cv2.imshow('webcam', img)
            #cv2.waitKey(1)

            #cv2.imshow('Taking Attendance', im)
            if (cv2.waitKey(1) == ord('q')):
                break

            #cv2.waitKey(1)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #cv2.destroyAllWindows()
            # cv2.imshow('webcam', img)
            #cv2.waitKey(0)
            #destroyWindow("webcam")


# After the loop release the cap object


# After the loop release the cap object

# button widget with red color text
# inside
btn = Button(root, text="Entry Attendance", width="20", pady=10,
             font="bold, 15",
             fg="#000000", command=clicked, bg='#6495ED', activeforeground='red', activebackground='blue')

btn.place(x=450,
          y=350)


def clicked():
    lbl3.configure(text="Exit Attendance Marked", fg="red")
    # vid = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture(0)

    vid = cv2.VideoCapture(0)
    while True:
            # Capture the video frame

            # by frame
            # ret, frame = vid.read()

            # Display the resulting frame
            # cv2.imshow('frame', frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            success, img = vid.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img,
                                #"Hershey Complex : ",
                                name,
                                (20, 160),
                                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                                fontScale=1,
                                color=(255, 255, 255))
                    l = name
                    engine.say('Good Bye ' + l)
                    # engine.say(l)
                    engine.runAndWait()
                    # cv2.putText(img,name(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                    markAttendanceex(name)
                    # vid.release()

            cv2.imshow('webcam', img)
            #cv2.waitKey(2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                destroyWindow("webcam")


btn2 = Button(root, text=" Exit Attendance", width="20", pady=10,
              font="bold, 15",
              fg="#000000", command=clicked, bg='#6495ED')

btn2.place(x=700,
           y=350)

datef = tk.Label(root, text=day + "-" + mont[month] + "-" + year + "  :", bg="#40E0D0", width=20, height=1,
                 font=('times', 30, ' bold '))
# datef.pack(fill='both',expand=1)#datef.pack(fill='both',expand=1)
datef.place(x=350,
            y=220)

clock = tk.Label(root, bg="#40E0D0", width=10, height=1, font=('times', 30, ' bold '))
# clock.pack(fill='both',expand=1)
clock.place(x=780,
            y=220)
tick()
# After t
btn4 = Button(root, text="QUIT", width="40", pady=10,
              font="bold, 15", command=root.destroy, bg='#6495ED')

btn4.place(x=500,
           y=720)
# define a video capture object

# Destroy all the windows


root.mainloop()