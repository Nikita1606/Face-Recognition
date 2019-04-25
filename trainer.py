# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 23:24:08 2019

@author: nikit
"""

import os
import cv2
import numpy as np
from PIL import Image

recogniser= cv2.face.LBPHFaceRecognizer_create()
path= "dataset"

def getimage(path):
    imagespath=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    ids=[]
    for imgpath in imagespath:
        faceImg=Image.open(imgpath).convert("L")
        size=(350,350)
        final_img=faceImg.resize(size,Image.ANTIALIAS)
        facenp=np.array(final_img,"uint8")
        ID=int(os.path.split(imgpath) [-1].split(".") [1])
        faces.append(facenp)
        print(ID)
        ids.append(ID)
        cv2.imshow("training",facenp)
        cv2.waitKey(100)
    return np.array(ids),faces

ids,faces= getimage(path)
recogniser.train(faces,ids)
recogniser.save("recogniser/trainingdata.yml")
cv2.destroyAllWindows()