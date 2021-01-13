#from tkinter import ttk
#import tkinter as tk
# 
# 
#def is_valid_char(char):
#    return char in "0123456789."
# 
# 
#root = tk.Tk()
#validatecommand = root.register(is_valid_char)
#entry = ttk.Entry(root, validate="key", validatecommand=(validatecommand, "%S"))
#entry.pack()
#root.mainloop()

#import cv2
#import os
#import numpy as np
#dataPath = './Data'#Cambia a la ruta donde hayas almacenado Data
#peopleList = os.listdir(dataPath)
#print('Lista de personas: ', peopleList)
#
#labels = []
#facesData = []
#label = 0
#
#for nameDir in peopleList:
#    personPath = dataPath + '/' + nameDir
#    print('Leyendo las imágenes')
#    
#    for fileName in os.listdir(personPath):
#        print('Rostros: ', nameDir + '/' + fileName)
#        labels.append(label)
#        facesData.append(cv2.imread(personPath+'/'+fileName,0))
#        image = cv2.imread(personPath+'/'+fileName,0)
#        cv2.imshow('image',image)
#        cv2.waitKey(10)
#        
#
#cv2.destroyAllWindows()

import cv2
import os

dataPath = './Data'#Cambia a la ruta donde hayas almacenado Data
imagePaths = os.listdir(dataPath)
    print('imagePaths=',imagePaths)
    
    reconocimiento = cv2.face.LBPHFaceRecognizer_create()
    
    # Leyendo el modelo
    reconocimiento.read('Entrenamiento.xml')
    
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    
    while True:
    	ret,Capturando = cap.read()
    	if ret == False: break
    	gray = cv2.cvtColor(Capturando, cv2.COLOR_BGR2GRAY)
    	auxCapturando = gray.copy()
    
    	faces = faceClassif.detectMultiScale(gray,1.3,5)
    
    	for (x,y,w,h) in faces:
    		rostro = auxCapturando[y:y+h,x:x+w]
    		rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
    		result = reconocimiento.predict(rostro)
    
    		cv2.putText(Capturando,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
    		
    		# LBPHFace
    		if result[1] < 70:
    			cv2.putText(Capturando,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
    			cv2.rectangle(Capturando, (x,y),(x+w,y+h),(0,255,0),2)
    		else:
    			cv2.putText(Capturando,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
    			cv2.rectangle(Capturando, (x,y),(x+w,y+h),(0,0,255),2)
    		
    	cv2.imshow('Capturando',Capturando)
    	k = cv2.waitKey(1)
    	if k == 27:
    		break
    
    cap.release()
    cv2.destroyAllWindows()