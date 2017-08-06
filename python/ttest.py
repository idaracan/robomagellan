from vision import cono
from socket import *
from bbbgps import *
from navegacion import *
from haversine import *
import thread
import time
import sys

#arriba = [11.020289, -74.848016]
#abajo  = [11.020035, -74.848057]
#izquierda=[11.020194, -74.848468]
#derecha = [11.020127, -74.847667]
dest  = [11.01796,-74.85141]
inicio= [11.01807,-74.85141]
punto2= [11.01826,-74.85138]

#triang(dest,newpos,pos)
a= int(triang(dest,inicio,[11.01807,-74.85142]))
a= a*1600/360
print a
print haversine(inicio,[11.01807,-74.85142])*1000
