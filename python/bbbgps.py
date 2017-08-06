import serial
from time import sleep
import sys
from socket import *
def read():
	while True:
		try:
			ser=serial.Serial('/dev/ttyUSB0',9600)	
			break
		except:
			sys.stdout.write('')

	IPv4 = "localhost"
	Port = 3004 
	ServerSock = socket(AF_INET, SOCK_DGRAM)			
	a = 0.0
	b = 0.0
	ser.flushInput()
	ser.flushInput()
	while True:
		while ser.inWaiting()==0:
				pass
		NMEA1=ser.readline()
		NMEA1_array= NMEA1.split(',')
		if NMEA1_array[0]=='$GPRMC':
			#latitude
				 latDeg=NMEA1_array[3][:-8]
				 latMin=NMEA1_array[3][-8:]
				 latHem=NMEA1_array[4]
			#longitude
				 lonDeg=NMEA1_array[5][:-8]
				 lonMin=NMEA1_array[5][-8:]
				 lonHem=NMEA1_array[6]
		if NMEA1_array[0]=='$GPGGA':
				 sats=NMEA1_array[7]
				 fix=NMEA1_array[6]

			#print myGPS.NMEA1
		try:
			if fix!=0:				
				#print 'You are Tracking: ',sats,' satellites'
				#print 'My Latitude: ',myGPS.latDeg, 'Degrees ', myGPS.latMin,' minutes ', myGPS.latHem
				#print 'My Longitude: ',myGPS.lonDeg, 'Degrees ', myGPS.lonMin,' minutes ', myGPS.lonHem
				try:
					a= (float((float(latDeg)) + float(latMin) / 60))
					b= (float((float(lonDeg)) + float(lonMin) / 60))
					if latHem == "S":
						a = -a
					if lonHem == "W":
						b = (-1)*b
					latitud = str("{0:.5f}".format(a))
					longitud= str("{0:.5f}".format(b))
					MESSAGE = latitud + ","+ longitud
					#print MESSAGE
					#MESSAGE = "11.12345,-74.12345"
					ServerSock.sendto(MESSAGE, (IPv4, Port))
				except Exception, e:
					sys.stdout.write('')
		except Exception, ex:
			sys.stdout.write('')
