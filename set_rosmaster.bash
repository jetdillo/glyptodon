#!/bin/bash 
#this is a first whack at trying to figure out where the ROS Master (probably) is
#mostly I got annoyed with constantly having to change it from localhost 
#to whatever IP the master was on
#This is horribly insecure, but then again, so is most of ROS at this point
DEFAULT_IFACE=`netstat -rn|grep UG|awk '{print $8}'`
if [ -n $DEFAULT_IFACE ] 
  then 
     DEFAULT_NET=`ifconfig $THE_IFACE|grep -E "UP BROADCAST RUNNING" -B 3|awk '/inet / { split($2,addr,":");split(addr[2],sn,".");printf("%s.%s.%s\n",sn[1],sn[2],sn[3]) }'`
     DEFAULT_MASTER=`nmap -p 11311 $DEFAULT_NET.0/24|awk 'BEGIN {rmstat=0} /Nmap scan report/ { robotip=$5;rmstat=rmstat+1;getline;getline;getline;if ($2=="open") { printf("%s:%d\n",robotip,11311)  } }'`
   else 
       echo "No default network and --guess not implemented\n...exiting"
       exit
fi

if [ ! -z $DEFAULT_MASTER ]
  then
      MASTER_COUNT=`echo $DEFAULT_MASTER|wc -l`
      if [ $MASTER_COUNT -eq 1 ]
      then
	export ROS_MASTER_URI="http://$DEFAULT_MASTER"
      elif [ $MASTER_COUNT -gt 1 ] 
   	   then 
              echo "Found $MASTER_COUNT ROS Masters at:\n $DEFAULT_MASTER\n ...using first encountered"
	      export ROS_MASTER_URI="http://`echo $MASTERS|head -1`"
	   fi
  else
	echo "Expected to find 1 ROS Master, found 0"
	echo "Falling back to localhost as ROS_MASTER (This is probably not what you want)"
	export ROS_MASTER_URI="http://localhost:11311"
fi
