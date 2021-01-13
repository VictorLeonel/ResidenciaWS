from tkinter import messagebox as MessageBox
import cv2,os
import imutils
import numpy as np
import tkinter as tk

root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")
root.configure(background="grey")
dataPath = './Data'

def Nota():
    MessageBox.showinfo("Nota", "Tomar encuenta que 400 capturas serian las recomendadas para que el sistema te identifique"+ 
                        "con cambios de iluminacion y gestos")
#Menú superior
menubar = tk.Menu(root)
menubar.add_cascade(label="Nota",command=Nota,)

def Validar(char):
    return char in "0123456789."

validatecommand = root.register(Validar)
Nombres = tk.StringVar()
Capturas = tk.IntVar()


label = tk.Label(root, text="Reconocimiento Facial",font=("times new roman",20),fg="white",bg="maroon",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

label = tk.Label(root, text="Nombre:",font=("times new roman",20),fg="white",bg="maroon").grid(row=2,sticky=N+E+W+S,padx=5,pady=5)
txt = tk.Entry(root,textvariable = Nombres, width=40, font=("times new roman",20),fg="black",bg="light blue").grid(padx=5, row=2, column=1)

label = tk.Label(root, text="Capturas:",font=("times new roman",20),fg="white",bg="maroon").grid(row=3,sticky=N+E+W+S,padx=5,pady=5)
txt1 = tk.Entry(root,validate="key",textvariable = Capturas,validatecommand=(validatecommand, "%S"), width=40, font=("times new roman",20),fg="black",bg="light blue").grid(padx=5, row=3, column=1)




def CapturarRostros():
 
   if Nombres.get()=="" or Capturas.get()=="" or Capturas.get()==0:
            MessageBox.showerror("Cuidado","No puede dejar los cuadros de entrada vacíos y Las Capturas tienen que ser mayor a 0")
   else:
    Nombre=(Nombres.get())
    Captura=(Capturas.get())
    personPath = dataPath + '/' + Nombre 
    

    if not os.path.exists(personPath):
    	print('Carpeta Creada: ',personPath)
    	os.makedirs(personPath)
        
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    count = 0
    
    while True:
    	ret, Capturando = cap.read()
    	if ret == False: break
    	Capturando =  imutils.resize(Capturando, width=640)
    	gray = cv2.cvtColor(Capturando, cv2.COLOR_BGR2GRAY)
    	auxCapturando = Capturando.copy()
    
    	faces = faceClassif.detectMultiScale(gray,1.3,5)
    
    	for (x,y,w,h) in faces:
    		cv2.rectangle(Capturando, (x,y),(x+w,y+h),(0,255,0),2)
    		rostro = auxCapturando[y:y+h,x:x+w]
    		rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
    		cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
    		count = count + 1
    	cv2.imshow('Capturando',Capturando)
    
    	k =  cv2.waitKey(1)
        if k == 27 or count >= Captura: 
    		break


    cap.release()
    cv2.destroyAllWindows()


def EntrenarSistema():
    
    peopleList = os.listdir(dataPath)
    print('Lista de personas: ', peopleList)
    
    labels = []
    facesData = []
    label = 0
    
    for nameDir in peopleList:
    	personPath = dataPath + '/' + nameDir
    	print('Leyendo las imágenes')
    
    	for fileName in os.listdir(personPath):
    		print('Rostros: ', nameDir + '/' + fileName)
    		labels.append(label)
    		facesData.append(cv2.imread(personPath+'/'+fileName,0))
    	label = label + 1
    
    reconocimiento = cv2.face.LBPHFaceRecognizer_create()
    
    # Entrenando el reconocedor de rostros
    print("Entrenando...")
    MessageBox.showinfo("Mensaje", "Entrenando el Sistema Espere a que aparesca el Mensaje de Almacenado Esto puede tardar dependiendo de cuantos datos hay capturados")
    reconocimiento.train(facesData, np.array(labels))
    
    # Almacenando el modelo obtenido
    reconocimiento.write('Entrenamiento.xml')
    print("Modelo Almacenado...")
    MessageBox.showinfo("Mensaje", "Modelo Almacenado...")


def Reconocimiento():

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

def Cerrar():

    root.destroy()
    
def limpiar():
    txt.tk.delete(0, tk.END)    
    txt1.tk.delete(0, tk.END)
    
    
    
    
#button = tk.Button(root,text="Limpiar",font=("times new roman",20),bg="#0D47A1",fg='white',command=limpiar).grid(row=4,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

button = tk.Button(root,text="Capturando Nuevo Registro",font=("times new roman",20),bg="#0D47A1",fg='white',command=CapturarRostros).grid(row=5,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
button = tk.Button(root,text="Entrenar Reconocimiento",font=("times new roman",20),bg="#0D47A1",fg='white',command=EntrenarSistema).grid(row=6,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
button = tk.Button(root,text="Ejecutar Reconocimiento",font=('times new roman',20),bg="#0D47A1",fg="white",command=Reconocimiento).grid(row=7,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
button = tk.Button(root,text="Exit      (╯ ° □ °) ╯︵ ┻━┻ ",font=('times new roman',20),bg="maroon",fg="white",command=Cerrar).grid(row=8,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

root.config(menu=menubar)
root.mainloop()