# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 22:41:14 2019

@author: nikit
"""

import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3

recogniser= cv2.face.LBPHFaceRecognizer_create()
recogniser.read("recogniser/trainingdata.yml")
cascadesPath="haarcascade_frontalface_default.xml"
facesCascade= cv2.CascadeClassifier(cascadesPath)
path= "dataset"

def getPerson(id):
    conn=sqlite3.connect("Facedb.db")
    comd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(comd)
    person=None
    for row in cursor:
       person=row
    conn.close()
    return person

cam= cv2.VideoCapture(0)
k=0
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
while True:
    ret,im =cam.read()
    if ret!=0:
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=facesCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(int(minW),int(minH)), flags = cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        id, conf= recogniser.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        if conf<100: #and conf<=85:
            print(id)
            person=getPerson(id)
            #cv2.putText(im, person[1], (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            print(conf)
            k=1
        else:
            k=0
        '''
        if(person!=None):
          print("person detected")'''
    cv2.imshow("img",im)
    cv2.waitKey(100)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break
    '''if k==1:
        print("person detected")
        cam.release()
        cv2.destroyAllWindows()
        break
    elif k==0:
        print("person not detected")
        cam.release()
        cv2.destroyAllWindows()
        break'''
