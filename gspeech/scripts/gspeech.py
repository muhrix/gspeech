#!/usr/bin/env python
#
# Author: Murilo FM
# Email:  muhrix@gmail.com
# 27 Dec 2013
# Based on the code written by:
#    achuwilson (https://github.com/achuwilson/gspeech)
#    korylprince (https://github.com/korylprince/python-google-transcribe)
#


#PACKAGE='gspeech'
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from gspeech_msgs.msg import Speech

import sys
import urllib2
import json
#import os
import subprocess
#import shlex

cmd1='sox -r 16000 -t alsa default recording.flac silence 1 0.1 60% 1 1.5 60%'
cmd2='wget -q -U "Mozilla/5.0" --post-file recording.flac --header="Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-GB"'

# For other language acronyms available for use with Google API, see:
# http://stackoverflow.com/questions/14257598/what-are-language-codes-for-voice-recognition-languages-in-chromes-implementati
language = 'en-GB' # en-US, pt-BR, pt-PT, ...
url_req = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang='+language

def speech():
	#rospy.init_node('gspeech')
    msg = Speech()

    try:
        ret = subprocess.call(cmd1, shell=True)
        if ret < 0:
            return
    except OSError as e:
        rospy.logerror('Command execution failed')
        return
    
    f = open('recording.flac')
    data = f.read()
    f.close()
    
    req = urllib2.Request(url_req, data, headers={'Content-type': 'audio/x-flac; rate=16000'})

    try:
        ret = urllib2.urlopen(req)
    except urllib2.URLError, e:
        # print ROS_ERROR and carry on
        rospy.logerror('urllib2 request error: %s'%e.reason)
        
    json_msg = json.loads(ret.read())
    print json_msg

    # status = 0 means something was recognised
    # it appears that status = 5 means that nothing could be
    # recognised, but sox recording and urllib2 requests worked
    if json_msg['status'] == 0:
        msg.speech = json_msg['hypotheses'][0]['utterance']
        msg.confidence = json_msg['hypotheses'][0]['confidence']
        pubm.publish(msg)
        #text = json_msg['hypotheses'][0]['utterance']
        #print text
    else if json_msg['status'] == 5:
        rospy.loginfo('Could not transcribe spoken line')
            

#	pubs = rospy.Publisher('speech', String)
#	pubc = rospy.Publisher('confidence', Int8)
	
#	args2 = shlex.split(cmd2)
	
#	os.system('sox -r 16000 -t alsa default recording.flac silence 1 0.1 1% 1 1.5 1%')	
#	output,error = subprocess.Popen(args2,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
		
#	if not error and len(output)>16:
#		a = eval(output)
#		if a['hypotheses']:
#			confidence= a['hypotheses'][0]['confidence']
#			confidence= confidence*100
#			data=a['hypotheses'][0]['utterance']
#                       msg.speech = data
#                       msg.confidence = confidence
#			pubm.publish(msg)
#			pubs.publish(String(data))
#			pubc.publish(confidence)
#			print String(data), confidence
	
    speech()	
	


if __name__ == '__main__':
    try:
        rospy.init_node('gspeech')
        pubm = rospy.Publisher('spoken_line', Speech)
        speech()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        sys.exit(1)
