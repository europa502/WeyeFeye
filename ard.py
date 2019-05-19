import serial
import syslog
import time

#The following line is for serial over GPIO
port = '/dev/ttyACM14'

angle=10
ard = serial.Serial(port,9600,timeout=0.1)
for angleLR in range(10,90):
	for angleTB in range(50,170):
		data="<"+str(angleLR)+","+str(angleTB)+">"	 
		ard.write(data)
		#print ard.readline()
		print data
		time.sleep(0.5)
