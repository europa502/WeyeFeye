import serial
import syslog
from scapy.all import *
from netaddr.core import NotRegisteredError
from netaddr import *
import threading
import os, time,argparse

class WeyeFeye:
	
	
	def __init__(self,port,iface):
		self.port=port
		self.iface=iface
		self.screenlock = threading.Semaphore(value=1)
	def hopper(self):
	    n = 1
	    stop_hopper = False
	    while not stop_hopper:
	    	for n in range (1,14):
			time.sleep(0.50)
			os.system('iwconfig %s channel %d' % (self.iface, n))
			self.screenlock.acquire()
			print "Current Channel %d" % (n)
	    	        self.screenlock.release()

	def PacketHandler(self,pkt) :
	   
	   #print "PacketHandler"
	   #print pkt.type, pkt.subtype
	   if pkt.type == 0 and pkt.subtype == 8:
	     	try:
		    
		    extra = pkt.notdecoded
		    rssi = -(256-ord(extra[-2:-1]))
		    #print "rssi", rssi
		except:
		    rssi = -100
		self.screenlock.acquire()
		print "BSSID:    ","WiFi signal strength:", rssi, "dBm of", pkt.addr2, pkt.info, os.popen('iwlist ' +self.iface+' channel').read()[-13:][:-2]
		
		self.screenlock.release()
		
	   '''if pkt.type==0 and pkt.subtype == 4:
		try:
		    
		    extra = pkt.notdecoded
		    rssi = -(256-ord(extra[-2:-1]))
		    #print "rssi", rssi
		except:
		    rssi = -100
		screenlock.acquire()
		print "STATION:  ","WiFi signal strength:", rssi, "dBm of",pkt.addr2,  pkt.info
		screenlock.release()
		
	      '''  	
	def parse(self,frame):
	    if frame.haslayer(Dot11):
		print("ToDS:", frame.FCfield & 0b1 != 0)
		print("MF:", frame.FCfield & 0b10 != 0)
		print("WEP:", frame.FCfield & 0b01000000 != 0)
		print("src MAC:", frame.addr2)
		print("dest MAC:", frame.addr1)
		print("BSSID:", frame.addr3)
		print("Duration ID:", frame.ID)
		print("Sequence Control:", frame.SC)
		#print(feature(frame))
		print("\n")
		
	def run_sniffer(self):        
		sniff(iface=self.iface, prn = wifi.PacketHandler)


	def serial_controller(self):
		#The following line is for serial over GPIO
		port = '/dev/tty'+self.port

		angle=10
		ard = serial.Serial(port,9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,)
		ard.flush()
		for angleTB in range(0,90):
			for angleLR in reversed(range(50,170)):
				data="<"+str(angleTB)+","+str(angleLR)+">"	 
				ard.write(data)
				check="turning servo to "+str(angleTB)+","+str(angleLR)+ " degrees"
				self.screenlock.acquire()
				print check
				print ard.readline()
				#if check in ard.readline():
				#	print "yes"
				#print ard.readline()
				#print "turning servo to "+str(angleTB)+","+str(angleLR)+ " degrees\n"
				print data
				self.screenlock.release()
				ard.flush()
				time.sleep(1)
				
if __name__ == '__main__':

	
	parser = argparse.ArgumentParser()
		
	parser.add_argument('-p','--port',type=str,default='', help='Arduino port')
	parser.add_argument('-i','--iface',type=str,default='', help='monitor interface')
	iface= parser.parse_args().iface
	port= parser.parse_args().port
	
	wifi=WeyeFeye(port,iface)
	thread1=threading.Thread(target=wifi.hopper, name="hopper")
	thread2=threading.Thread(target=wifi.run_sniffer, name="run_sniffer")
	thread3=threading.Thread(target=wifi.serial_controller, name="controller")	

    #thread1.daemon = True
   	thread1.start()
    	thread2.start()
    	thread3.start()
    #thread4.start()
    #thread5.start()
    #thread6.start()
	print  "thread started"
