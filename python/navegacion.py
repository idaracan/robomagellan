import sys
import math
import serial
import time

def triang(dest,actpos,antpos):
	dest[0] = float(dest[0])
	dest[1] = float(dest[1])
	
	actpos[0]=float(actpos[0])
	actpos[1]=float(actpos[1])
	
	antpos[0]=float(antpos[0])
	antpos[1]=float(antpos[1])
	#dest[1]=longitude of destination
	#dest[0]= latitude of destination
	
	#antpos[1]=longitude of previous position
	#antpos[0]= latitude of previous position
	
	#actpos[1]=longitude of actual position
	#actpos[0]= latitude of actual position
	
	#Length of sides of the triangle
	try:
		A = math.sqrt(((antpos[0]-dest[0])**2)+((antpos[1]-dest[1])**2))
		B = math.sqrt(((antpos[0]-actpos[0])**2)+((antpos[1]-actpos[1])**2))
		C = math.sqrt(((actpos[0]-dest[0])**2)+((actpos[1]-dest[1])**2))
	
		#finding out the angles
		a = math.degrees(math.acos(((A**2)-(B**2)-(C**2))/(-2*C*B))) #Angulo opuesto de A
		b = math.degrees(math.acos(((B**2)-(A**2)-(C**2))/(-2*A*C))) #Angulo opuesto de B
		c = math.degrees(math.acos(((C**2)-(A**2)-(B**2))/(-2*A*B))) #Angulo opuesto de B
		
		x = -1*(180-a)
		y = (180-a)
		print "Lados: "
		print A
		print B
		print C
		print "Angulos: "
		print x
		print y
		#cases of operation
		#case 1
		if ((actpos[1]>antpos[1] and actpos[1] > dest[1] and antpos[1]>dest[1] and antpos[0] < dest[0] and antpos[0] < dest[0])):
			ang= x
		#case 2
		elif (dest[1]<actpos[1]<antpos[1] and antpos[0]>actpos[0]<dest[0]):
			ang= y
		#case 3
		elif (dest[1]>actpos[1]>antpos[1] and dest[0]>actpos[0]<antpos[0]):
			ang= x
		#case 4
		elif (dest[1]>actpos[1]<antpos[1] and dest[0]>antpos[0]<actpos[0]):
			ang= y
		#case 5
		elif (dest[1]>actpos[1]<antpos[1] and antpos[0]>dest[0]<actpos[0]):
			ang= x
		#case 6
		elif (dest[1]<actpos[1]>antpos[1] and antpos[0]>dest[0]<actpos[0]):
			ang= y
		#case 7
		elif (dest[1]<actpos[1]>antpos[1] and dest[0]<antpos[0]>actpos[0]):
			ang= y
		#case 8
		elif (dest[1]<antpos[1]>actpos[1] and antpos[0]<actpos[0]>dest[0]):
			ang= x
		#case 9
		elif (dest[1]>antpos[1]<actpos[1] and antpos[0]<actpos[0]>dest[0]):
			ang= y
		#case 10
		elif (dest[1]>antpos[1]>actpos[1] and actpos[0]<antpos[0]>dest[0]):
			ang= x
		#case 11
		elif (antpos[1]>dest[1]>actpos[1] and actpos[0]<dest[0]>antpos[0]):
			ang= y
		#case 12
		elif (dest[1]>antpos[1]<actpos[1] and actpos[0]<dest[0]>antpos[0]):
			ang= x
		else:
			ang =y
		#print ang
	except:
		ang = 10
	return round(ang)
