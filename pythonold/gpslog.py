def listen():
	while True:
		try:
			latlng, addr = ServerSockGPS.recvfrom(1024) # buffer size is 1024 bytes
			#print type(latlng)	
			if latlng == "":
				print "null"
			else:
				latlng = latlng.split(",")
				return latlng
		except NameError:
			sys.stdout.write('')
			
from vision import cono
from socket import *
from bbbgps import *
from navegacion import *
from haversine import *
#from navegacion import *
import thread
import time
import sys
#GPS socket
gpsPort = 3004 #"""puerto a olfatear"""
ServerSockGPS = socket(AF_INET, SOCK_DGRAM) 
ServerSockGPS.bind(("localhost",gpsPort))
latlng = ""

#Starts GPS
thread.start_new_thread(read, ())
while (1):
	print listen();
