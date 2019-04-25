# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:53:23 2019

@author: nikit
"""
import cv2
import sqlite3

cam=cv2.VideoCapture(0)
detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def InsertorUpdate(id,phoneno):
    conn=sqlite3.connect("Facedb.db")
    comd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(comd)
    Recordexists=0
    for row in cursor:
       Recordexists=1
    if(Recordexists==1):
        comd="UPDATE People SET PHONENO="+str(phoneno)+" WHERE ID="+str(id)
    else:
        comd="INSERT INTO People(ID,PHONENO) Values("+str(id)+","+str(phoneno)+")"
    conn.execute(comd)
    conn.commit()
    conn.close()
    
id= int(input("enter your userid:"))
phoneno= int(input("enter your phoneno:"))
InsertorUpdate(id,phoneno)
sampleNum=0
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1
        cv2.imwrite("dataset/user."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
    cv2.imshow("img",im)
    cv2.waitKey(5)
    if sampleNum>500:
        cam.release()
        cv2.destroyAllWindows()
        break
    