def listen():
	while True:
		try:
			latlng, addr = ServerSockGPS.recvfrom(18) # buffer size is 1024 bytes
			#print "El gps da esto> ", latlng	
			#latlng = coordenadasdos()
			#latlng=raw_input("entre coordenadas> ")
			if latlng == "":
				sys.stdout.write('')
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
print "-----begining of program-----"
dest =  [11.02015, -74.84800]#[11.01995, -74.82368] PARQUE BV#[11.02230, -74.85150] PARQUEADERO 12 #[11.02055, -74.85156] DETRAS DEL K K#[11.02008, -74.84798]CANCHA DE FUTBOL
print "destino: ",dest

while True:
	try:
		Arduino = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=None)
		print "Arduino Ok "
		break
	except Exception, e:
		sys.stdout.write('')
		#print "Error Arduino: ", str(e) 

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
send_this = ""
newpos = [0.0,0.0]
pos = [0.0,0.0]

pos	 = listen()#[11.01999,-74.84818] 

while True:	
	print "pos: ",str(pos)
	Arduino.write("u") #forward
	newpos = listen()#[11.02004,-74.84796]
	print "newpos ",newpos
	recorrido = haversine(pos,newpos) * 1000
	dist   	  = haversine(dest,newpos)* 1000
	print "distancia recorrida: ",recorrido
		
	if (recorrido>3):
		print "newpos: ",newpos
		angulo = int(triang(dest,newpos,pos))
		print "angulo a girar: ",angulo
		angulo = int(angulo * 1600 / 360 )
		tiempo = int(round(angulo/45))
		
		if (angulo < 0):
			send_this = negativo * (-tiempo)
		else:
			send_this = positivo * tiempo
		print "se manda al arduino: ",send_this
		Arduino.write(str(send_this))
		pos = newpos
		
	print "dist: ",dist
	
	if (dist < 5):
		Arduino.write(negativo)
		print "acercandose"
		break
	
time.sleep(1)
#for distances less than 10m
Arduino.write("g")
time.sleep(1)
thread.start_new_thread(cono, ())
i=1
while True:
	newpos = listen()
	try:
		data, addr = ServerSockCamera.recvfrom(1024)
		data = data.split(",")
		print data[0]
		x = float(data[0])
		#print type(x)
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
		Arduino.write("++++")
		sys.stdout.write('')
	
	if (newpos == dest):
		Arduino.write("s")
		break
print "-----end of program-----"
