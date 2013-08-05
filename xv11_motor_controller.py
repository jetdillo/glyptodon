#!/usr/bin/env python
"""Basic PWM Software controller for Neato LDS
   Requirements: bare Neato LDS(no logic board)
                 patched/modified CWRU xv_11_laser_driver package
		 that implements/exposes an rpm topic
		 Make Controller board
"""


import sys,os,serial,socket
import getopt

import rospy
from std_msgs.msg import UInt16

import mcontroller
import pdb

class motorctlr (object):
	results=0	
	haslaser=0
	rpmport=0
	pulseduty=0
	minrpm=295
	maxrpm=310
        rpmcltr=''
 	
	def __init__(self,addr):
	#set up internal variables and just return a "stub" object
	#we expect laserport to be a handle to an already open serial.Serial object
	    self.results=0
	    self.haslaser=0
	    self.pulseduty=768
	    self.minrpm=295
	    self.maxrpm=320
	    self.bootstep=20
	    self.rpmcheck=0 
	    self.rpmsamples=[]
            try:
	       self.rpmctlr=mcontroller.AppBoard(addr)
	       self.rpmctlr.set_pwm(0,self.pulseduty,'duty')
	    except:
               sys.exit("Failed to set PWM on Controller")
		   
	def rpmctl(self,currpms,step,samples):
	    rpmval=0
            if(len(self.rpmsamples) < samples):
               self.rpmsamples.append(currpms)
            else:
               mean_rpms=(sum(self.rpmsamples))/samples
	       self.rpmsamples=[]
 
	       if mean_rpms < self.minrpm :
                  self.pulseduty += step

	       if mean_rpms > self.maxrpm :
		  self.pulseduty -= step
	
	       if mean_rpms < self.maxrpm:
       	          self.pulseduty +=1            

	       try:
		  self.rpmctlr.set_pwm(0,self.pulseduty,'duty')
		  print ("current RPM %d pulseduty= %d" ) % (mean_rpms,self.pulseduty)
               except:
		  print "Failed to set PWM on Controller"
		  exit()
