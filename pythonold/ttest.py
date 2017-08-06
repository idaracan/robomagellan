from vision import cono
from socket import *
from bbbgps import *
from navegacion import *
from haversine import *
#from navegacion import *
import thread
import time
import sys

#arriba = [11.020289, -74.848016]
#abajo  = [11.020035, -74.848057]
#izquierda=[11.020194, -74.848468]
#derecha = [11.020127, -74.847667]
#dest  = [11.01796,-74.85141]
#inicio= [11.01807,-74.85141]
#punto2= [11.01826,-74.85138]

#triang(dest,newpos,pos)
#a= int(triang(dest,punto2,inicio))
#a= a*1600/360
#print a,type(a)
#print haversine(inicio,punto2)*1000

#Camera socket
IPv4 = "localhost" #"""IP del servidor""" 
camPort = 3003 #"""puerto a olfatear""" 
ServerSockCamera = socket(AF_INET, SOCK_DGRAM) 
ServerSockCamera.bind((IPv4,camPort)) 
data = ""
addr = ""

x = 0.0
y = 0.0

print "camera socket init"

while True:
	try:
		Arduino = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=None)
		break
	except:
		sys.stdout.write('')
print "arduino connected"
thread.start_new_thread(cono, ())
i=1
positivo = "+"
negativo = "-"
print "searching"
while True:
	try:
		data =""
		while data=="" : #If haven't recieved data
			data, addr = ServerSockCamera.recvfrom(1024)
			if data != "":
				break
			
			if i%2 == 0:
				Arduino.write(positivo*i)
			else:
				Arduino.write(negativo*i)
			time.sleep(i)
			i += 1
			if i > 6:
				i=1
		#when position data is recieved
		print data
		data=data.split(",")
		x = float(data[0])
		print x
		if (x<20):
			Arduino.write(positivo) 
			print "derecha"
		elif(x>20):
			Arduino.write(negativo)
			print "izquierda"
		time.sleep(1)
		Arduino.write("f")
	except:
		sys.stdout.write('')

