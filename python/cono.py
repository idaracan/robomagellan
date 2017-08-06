import cv2
import numpy as np
from socket import *
import sys
import time
def cono():
	
	#IPv4 = "localhost"
	#Port = 3003 
	#ServerSock = socket(AF_INET, SOCK_DGRAM)
			
	#OpenCV Version
	print "Opencv Version: {0}".format(cv2.__version__)
	#Iniciamos la camara
	captura = cv2.VideoCapture(0)
	#
	#resolucion
	captura.set(3,320)
	captura.set(4,240)
	#FPS
	#captura.set(5,10)
	time.sleep(5)
	triangulo = False
	if(captura.isOpened()):
		print "Capturing Image"
	while(1):
		
		#Capturamos una imagen y la convertimos de RGB -> HSV
		_,imagen = captura.read()
		hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
		#15, 255, 232	safety orange
		#15, 255, 255	orange color
		#Establecemos el rango de colores que vamos a detectar (Naranja, RGB 0-255)
		naranja_bajos = np.array([0, 115, 154], dtype=np.uint8)
		naranja_altos = np.array([15, 192, 255], dtype=np.uint8)
		
		#Mascara color naranja
		mask = cv2.inRange(hsv, naranja_bajos, naranja_altos)
		
		#Filtrar Imagen
		kernel = np.ones((6,6),np.uint8)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		
		#Calcular el area del objeto observado
		moments = cv2.moments(mask)
		area = moments['m00']
		
		#Gausiano-canny, Contornos, areas 
		blur = cv2.GaussianBlur(mask, (5, 5), 0)
		edges = cv2.Canny(mask,1,2)
		_, contours, _= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		areas = [cv2.contourArea(c) for c in contours]
		
		i = 0
		for extension in areas:
		   if extension > 600:
			  actual = contours[i]
			  #Aproximar el numero de vertices
			  approx = cv2.approxPolyDP(actual,0.05*cv2.arcLength(actual,True),True) # Douglas-Peucker
			  #Si tiene 3 vertices, es un triangulo
			  triangulo = False
			  if len(approx)==3:
				  cv2.drawContours(imagen,[actual],0,(0,0,255),2)
				  triangulo = True
		   i = i+1    
		
		#Generar punto en un area > 20000
		try:
			
			if(area > 20000):# and (triangulo == True):

				#Buscamos y mostramos coordenadas x y y del objeto
				x = int(moments['m10']/ moments['m00'])
				y = int(moments['m01']/ moments['m00'])
				xi = x - (captura.get(3) / 2)
				yi = y - (captura.get(4) / 2)
				MESSAGE = str(-xi) + ","+ str(-yi)
				#Dibujamos una marca roja en el centro del objeto
				cv2.rectangle(imagen, (x, y), (x+2, y+2), (0,0,255), 2)
				cv2.rectangle(mask, (x, y), (x+2, y+2), (0,0,255), 2)
				#print captura.get(5)
			else:
				MESSAGE = ""
			#ServerSock.sendto(MESSAGE, (IPv4, Port))
			print MESSAGE
		except:
			sys.stdout.write('')
				
		#Mostramos la imagen original con la marca del centro y
		#la mascara
		cv2.imshow('mask', mask)
		cv2.imshow('Camara', imagen)
		tecla = cv2.waitKey(5) & 0xFF
		if tecla == 27:
			break

	cv2.destroyAllWindows()

