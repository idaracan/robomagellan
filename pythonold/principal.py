def listen():
	while True:
		try:
			latlng, addr = ServerSockGPS.recvfrom(1024) # buffer size is 1024 bytes
			#print type(latlng)	
			#latlng = coordenadasdos()
			if latlng == "":
				print "null"
			else:
				latlng = latlng.split(",")
				latlng[0]=float(latlng[0])
				latlng[1]=float(latlng[1])
				return latlng
		except NameError:
			sys.stdout.write('')
			#print str(NameError)

def coordenadas():
	coordenadas = open('coordenadas.txt','r')
	coordenadas = coordenadas.readline()
	coordenadas = coordenadas.split(",")
	coordenadas[0] = float(coordenadas[0])
	coordenadas[1] = float(coordenadas[1])
	return coordenadas

def coordenadasdos():
	coordenadas = open('coordenadasdos.txt','r')
	coordenadas = coordenadas.readline()
	coordenadas = coordenadas.split(",")
	coordenadas[0] = float(coordenadas[0])
	coordenadas[1] = float(coordenadas[1])
	return coordenadas


import sys
import thread
import math
import serial
import time
from haversine import haversine	
from cono import cono
from socket import *
from bbbgps import *
from navegacion import *

dest = coordenadas()
print "destino: ",dest

while True:
	try:
		Arduino = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=None)
		break
	except:
		sys.stdout.write('')

IPv4 = "localhost" #"""IP del servidor""" 

#Camera socket
camPort = 3003 #"""puerto a olfatear""" 
ServerSockCamera = socket(AF_INET, SOCK_DGRAM) 
ServerSockCamera.bind((IPv4,camPort)) 
data = ""
addr = ""

x = 0.0
y = 0.0

#GPS socket
gpsPort = 3004 #"""puerto a olfatear"""
ServerSockGPS = socket(AF_INET, SOCK_DGRAM) 
ServerSockGPS.bind((IPv4,gpsPort))
latlng = ""

#Starts GPS
thread.start_new_thread(read, ())

angulo = 0.0
global i
i = 1 
cont = 1

positivo = "+"
negativo = "-"

newpos = [0.0,0.0]

while True:	
	Arduino.write("u") #forward
	time.sleep(3)
	pos	 = listen()
	print "pos: ",pos
	newpos = listen() #[0] = pos[0] + 0.0001
	#newpos[1] = pos[1] #listen() 
	
	recorrido = haversine(newpos,pos) * 1000
	dist   =    haversine(dest,newpos)* 1000
	
	print "distancia recorrida: ",recorrido
	
	if (recorrido>5):
		print "newpos: ",newpos
		angulo = int(triang(dest,newpos,pos))
		angulo = int(angulo * 1600 / 360 )
		if (angulo > 0):
			tiempo = int(round(angulo/45))
			tiempo = positivo * tiempo
		else:
			tiempo = -1*int(round(angulo/45))
			tiempo = negativo * tiempo
		print tiempo
		Arduino.write(str(tiempo))
		time.sleep(2)
		print "angulo: ",angulo
		
	print "dist: ",dist
	
	if (dist < 10):
		Arduino.write("s")
		print "acercandose"
		break
time.sleep(1)
#for distances less than 10m
Arduino.write("g")
time.sleep(1)
thread.start_new_thread(cono, ())
i=1
while True:
	try:
		data, addr = ServerSockCamera.recvfrom(1024)
		data = data.split(",")
		print data[0]
		x = float(data[0])
		print type(x)
		if x>10.0:
			Arduino.write(positivo)
			print positivo
		elif x<-10.0:
			Arduino.write(negativo)
			print negativo
		else:
			Arduino.write("u")
			print "hacia adelante"
	except:
		Arduino.write(positivo)
		sys.stdout.write('')
