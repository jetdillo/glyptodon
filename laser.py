#!/usr/bin/env python 
#laser.py 
# Copyright 2012 Stephen Okay for Roadknight Labs
# Released under the GNU GPL V2

"""
XV11 utils 
This program provides methods to get ranging data from a bare(i.e. not in a) Neato Robotics XV11 Laser Distance Scanner
running 2.6.x firmware
"""

import sys
import os 
import serial 
import socket

class laser (object):
	
	haslaser=0
	laserport=0
	laserlock_fd=''
	laserlock_sz=0
	mapnames=[]
	cmdmode=0

	def __init__(self,sd):
	#set up internal variables and just return a "stub" object
	#we expect laserport to be a handle to an already open serial.Serial object

		self.results=0
		self.haslaser=0
		self.laserport=sd
		
	def ack(self):
		ackbuf=0
		self.laserport.flushInput()		
		self.laserport.write("\r")
		ackbuf = self.laserport.read(3)
		if (ackbuf == "#"):
			self.laserport.flushInput()
			return 0
		else:
			return -1

	def read_debug(self):
        	while 1 : 
			  for x in xrange(0,21):
	  			serbyte=lp.read(1)
               		   	print hex(ord(serbyte)),
			  print "\n"

	def scanline_b(self,angle):
		headerpos=0
		scanline=0
		insync=0
		rpms=0	
		scandist=[]
		scanbytes=[]
		
		while insync == 0:
			headerbyte=ord(self.laserport.read(1))
			if headerbyte == 0xfa:
				scanbyte=ord(self.laserport.read(1))
				if scanbyte == angle:
					insync=1
		if insync == 1:
				try:
					scanbytes=[ord(self.laserport.read(1)) for x in xrange(0,19)]	
					scandist=[scanbytes[2],scanbytes[3],scanbytes[6],scanbytes[7],scanbytes[10],scanbytes[11],scanbytes[14],scanbytes[15]]	
				except IOError,e:
					print "Failed trying to read scanline %x" % scanhdr
		return scandist
	
        def read_hdr(self,curhdr):
		headerpos=0
		scanline=0
		insync=0
		self.laserport.flushInput()
                while insync == 0:
			headerbyte=ord(self.laserport.read(1))
                        #print "Expecting %x got %x" % (self.pinghdr[headerpos],headerbyte)
                        if headerbyte == 0xfa :
				scanbyte=ord(self.laserport.read(1))
				if scanbyte == curhdr:
				#	print "FOUND START OF SCAN %x with curhdr of %x " % (headerbyte,scanbyte)
					insync=1
		return True

	def slice(self,slicenum):
		headerpos=0
		scanline=0
		scanbytes=[]
		scanstr=''
		self.laserport.flushInput()
		try:
			self.read_hdr(slicenum)
			#scanstr = self.laserport.read(20)
			scanbytes = [ ord(self.laserport.read(1)) for x in xrange(0,20) ]

		except IOError,e:
			print "slice read failed trying to read header for %d" % slicenum
			return -1
		return scanbytes
	
	def errbits(self,errbyte):
		result=0
		if ((0x8000&(errbyte<<8))):
			result=1
		if ((0x4000&(errbyte<<8))):
			result=3
		return result
	
	def dump_scanline(self,scanpos,scanbuf):
		print("fa %x:") % scanhdr,
		for sb in scanbuf:
			disterr=l.errbits(sb)
			if(disterr == 0):
				print ("%x ") % sb,
			else:
				if(disterr == 1):
					print ("<>"),
				if(disterr == 3): 
					print ("><"),
		print

#Expect that the user has already filtered out too-close/too far distance errors from the bytestream
	def bytes_distance(self,scanbytes):
		return scanbytes[0]|(scanbytes[1]<<8)

	def scanline_distance(self,scanbuf):
		distances=[]
		for d in range((len(scanbuf))-1):
			distances.append(scanbuf[d]|(scanbuf[d+1]<<8))
		return distances

if __name__ == '__main__':
	

         try: 	
		lp= serial.Serial('/dev/ttyO1',115200,timeout=1)
	 except: 
		print "Could not open serial port for laser!"
		exit()

	 l = laser(lp)
	 scanhdr=0xa0
	 scanrange=[]
	 distdata=[]	
	 i=0
	 while 1: 
		try: 
			scanrange=l.scanline_b(scanhdr)
			print("%d:") % (scanhdr-0xa0),
			srlen= len(scanrange)
			for si in xrange(1,srlen,2):
				disterr=l.errbits(scanrange[si])
				if(disterr == 0):
					distdata=scanrange[si-1],scanrange[si]
					print l.bytes_distance(distdata),
				
			print
			if scanhdr == 0xf9:
				scanhdr=0xa0
			else:
				scanhdr+=1 
		except IOError,e:
			print "failed to read scanline %x" % scanhdr	
