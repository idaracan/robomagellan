import cv2
import numpy as np
from socket import *
import sys

def cono():
	#Camera startup
	captura = cv2.VideoCapture(0)
	#captura.set(3,340) height set
	#captura.set(4,480) width set
	#captura.set(5,15)  fps set
	
	#Setting a socket for communication
	IPv4 = "localhost"
	Port = 3003 
	ServerSock = socket(AF_INET, SOCK_DGRAM)
	
	while(1):
		#Image capture
		_, imagen = captura.read()
		hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
		#Colors to filter
		naranja_bajos = np.array([0, 115, 154], dtype=np.uint8)
		naranja_altos = np.array([15, 192, 255], dtype=np.uint8)
		
		#Mask
		mask = cv2.inRange(hsv, naranja_bajos, naranja_altos)
		
		#Aplying filter
		kernel = np.ones((6,6),np.uint8)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		
		#Area Calculation
		moments = cv2.moments(mask)
		area = moments['m00']
		
		#Gausiano-canny, Contornos, areas 
		blur = cv2.GaussianBlur(mask, (5, 5), 0)
		edges = cv2.Canny(mask,1,2)
		_,contours, _= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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
			if(area > 6000) and (triangulo == True):
				#Buscamos y mostramos coordenadas x y y del objeto
				x = int(moments['m10']/ moments['m00']) 
				y = int(moments['m01']/ moments['m00'])
				xi = x - (captura.get(3) / 2)
				yi = y - (captura.get(4) / 2)
				MESSAGE = str(-xi) + ","+ str(-yi)
			else:
				MESSAGE = ""
			ServerSock.sendto(MESSAGE, (IPv4, Port))
				#print MESSAGE #coordinate outputs
				#cv2.rectangle(imagen, (x, y), (x+2, y+2), (0,0,255), 2)
		except UnboundLocalError:
			sys.stdout.write('UnboundLocalError!')
			#Dibujamos una marca roja en el centro del objeto
		#Mostramos la imagen original con la marca del centro
		#cv2.imshow('Camara', imagen)
		#tecla = cv2.waitKey(5) & 0xFF
		#if tecla == 27:
		#	break

	#cv2.destroyAllWindows()
 
#cono()
