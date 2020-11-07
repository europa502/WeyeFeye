from serial import Serial
from scapy.all import *
from netaddr import *
import threading
import os, time, argparse
import time

class WeyeFeye:
	
	
	def __init__(self,port,iface,cal,ch):
		self.port='/dev/'+port
		self.iface=iface
		self.cal=cal
		self.channels=ch
		self.avail_ch=[]
		self.screenlock = threading.Semaphore(value=1)
		self.angle=10
		self.ard = Serial(self.port,9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,)
		self.ard.flush()
		self.position=""
		os.system("mkdir -p /root/weyefeye/data/")
		self.data_file= open("/root/weyefeye/data/data.csv","w+")
		self.data_file.write("BSSID,ESSID,RSSI,POSITION_Y,POSITION_X\n")
		if self.cal=="True" or self.cal=="true":
			self.ard.write("<@>")
			for lines in range(12):
				print (self.ard.readline())
			
	'''def basic_scan(self,pkt):
		if pkt.type == 0 and pkt.subtype == 8:
			try:
				extra = pkt.notdecoded
				rssi = -(256-ord(extra[-2:-1]))
				#print "rssi", rssi
			except:
				rssi = -100
		#self.screenlock.acquire()
		#print "BSSID:    ","WiFi signal strength:", rssi, "dBm of", pkt.addr2, pkt.info#, os.popen('iwlist ' +self.iface+' channel').read()[-13:][:-2]
	'''	
	def hopper(self):
		if self.channels=="all":
			while True:
				for n in range (1,14):
					time.sleep(1/13)
					os.system('iwconfig %s channel %d' % (self.iface, n))
					self.screenlock.acquire()
					print ("Current Channel %d" %n)
					self.screenlock.release()
	''' else:
	    	basic_scan()
	    	for i in self.avail_ch:
	    		time.sleep(1/len(self.avail_ch))
	    		os.system('iwconfig %s channel %d' % (self.iface, n))
			self.screenlock.acquire()
			print "Current Channel %d" % (n)
	    	        self.screenlock.release()
	    	'''	

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
	#self.screenlock.acquire()
	#print "BSSID:    ","WiFi signal strength:", rssi, "dBm of", pkt.addr2, pkt.info#, os.popen('iwlist ' +self.iface+' channel').read()[-13:][:-2]
	self.data_file.write(pkt.addr2+","+pkt.info+","+str(rssi)+","+self.position+"\n")

	#self.screenlock.release()

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


	def serial_controller(self,angleLR,angleTB):
				
				data="<"+str(angleTB)+","+str(angleLR)+">"	 
				self.ard.write(data)
				check="turning servo to "+str(angleTB)+","+str(angleLR)+ " degrees"
				self.screenlock.acquire()
				#print check
				#print ard.readline()
				if check in self.ard.readline():
					self.position=str(angleTB)+","+str(angleLR)
				#print check	
				#print self.ard.readline()
				self.screenlock.release()
				self.ard.flush()
				time.sleep(1)
	def sweeper(self):
		for angleTB in reversed(range(90,170)):
			for angleLR in (range(50,170)):
				self.serial_controller(angleLR,angleTB)
			for angleLR in reversed(range(50,170)):
				self.serial_controller(angleLR,angleTB)
			angleTB-=1
		
				
if __name__ == '__main__':

	
	parser = argparse.ArgumentParser()
		
	parser.add_argument('-p','--port',type=str,default='', help='Arduino port')
	parser.add_argument('-i','--iface',type=str,default='', help='Monitor interface')
	parser.add_argument('-k','--caliberate',type=str,default='false', help='Caliberate the Servoes')
	parser.add_argument('-c','--channels',type=str,default='restricted', help='Restrict scanning channels')
	iface= parser.parse_args().iface
	port= parser.parse_args().port
	cal=parser.parse_args().caliberate
	ch=parser.parse_args().channels
	wifi=WeyeFeye(port,iface,cal,ch)
	thread1=threading.Thread(target=wifi.hopper, name="hopper")
	thread2=threading.Thread(target=wifi.run_sniffer, name="run_sniffer")
	thread3=threading.Thread(target=wifi.sweeper, name="sweeper")	

	#thread1.daemon = True
	thread1.start()
	thread2.start()
	thread3.start()
	#thread4.start()
	#thread5.start()
	#thread6.start()
	print ( "thread started")
