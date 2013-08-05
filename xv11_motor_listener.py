#!/usr/bin/env python
import rospy
import getopt
from std_msgs.msg import UInt16

from xv11_motor_controller import motorctlr

"""A simple listener for the /rpm topic from the modified CWRU xv11_laser_driver"""
"""See xv11_motor_controller.py for parameters to the motorctlr object"""

def callback(data):
    rospy.loginfo(rospy.get_name() + ": Current Laser RPMs: %d" % data.data)
    mc.rpmctl(data.data,5,5)
 
def listener():
    rospy.init_node('pwm_control', anonymous=True)
    rospy.Subscriber("rpms", UInt16, callback)
    rospy.spin()

if __name__ == '__main__':
    ctlr_addr='192.168.2.12'
    
    global mc   #yes, yes,yes, abjure and abhore...later, after I get this working...
    mc=motorctlr(ctlr_addr)
    listener()
