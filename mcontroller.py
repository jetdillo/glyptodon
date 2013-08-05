#!/usr/bin/env python 
#makecontroller.py 
# Copyright 2012 Stephen Okay for Roadknight Labs
# Released under the GNU GPL V2

"""
Make Controller Interface
Basic command interface into the Making Things Make Controller board
"""

import sys
import os 
import serial 
import socket
import OSC

class  AppBoard(object):
	
	hasAB=0
	default_ip='192.168.2.10'
	listen=9000
        send=10000

	def __init__(self,addr):
	#set up internal variables and just return a "stub" object
	#we expect laserport to be a handle to an already open serial.Serial object
		
		self.results=0
		self.haslaser=0
		self.addr_t=(addr,self.listen)
		try:
	#tickle the OSC Client at addr to see if it responds
			oc=OSC.OSCClient()
			oc.connect(self.addr_t)
			oc.close()
		except:
			print("Could not connect to Controller at %s") % addr
			

	def send_message(self,msgstr,msgval):
		try:
			oc=OSC.OSCClient()
			oc.connect(self.addr_t)
			msg = OSC.OSCMessage()
			msg.setAddress(msgstr)
			msg.append(msgval)
			oc.send(msg)
			oc.close()
			results=0
		except :
			print ("send_message failed ") 
			results=-1

		return results
	
	def set_pwm(self,unit,value,cmd):
		keywords=['duty','invA','invB','active','dividerAValue','dividerAMux','dividerBValue','dividerBMux','clockSource','alignment','polarity']
		pwms=[0,1,2,3]
		
		if value >= 0 and value <=1023:
			if cmd in keywords and unit in pwms:
				msgstr="/pwmout/"+str(unit)+"/"+cmd
				print "sending %s %d" % (msgstr,value)
				results=self.send_message(msgstr,value)
			else:
				results=-1
		else:
			results=-1
		return results

	def set_appleds(self,unit,state):
		leds=[0,1,2,3]

		if unit in leds:
			msgstr="/appled/"+str(unit)+"/state "
			#msgstr="/appled/"+str(unit)+"/active "
			results=self.send_message(msgstr,state)
		else:
			results=-1
		return results

	def set_active(self,devstr,unit,state):
		
		msgstr=devstr+"/"+str(unit)+"/"+"active"
		result=self.send_message(msgstr,state)
	
