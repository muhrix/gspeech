#!/usr/bin/env python
#
# Author: Murilo FM
# Email:  muhrix@gmail.com
# 14 Dec 2013
# Based on the code written by:
#    achuwilson (https://github.com/achuwilson/gspeech)
#    korylprince (https://github.com/korylprince/python-google-transcribe)
#


PACKAGE='gspeech'
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8
from gspeech_msgs.msg import Speech

import sys
import urllib2
import json
import os

import shlex,subprocess

cmd1='sox -r 16000 -t alsa default recording.flac silence 1 0.1 1% 1 1.5 1%'
cmd2='wget -q -U "Mozilla/5.0" --post-file recording.flac --header="Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v1/recognize?lang=en-GB&client=chromium"'

# For other language acronyms available for use with Google API, see:
# http://stackoverflow.com/questions/14257598/what-are-language-codes-for-voice-recognition-languages-in-chromes-implementati
language = 'en-GB' # en-US, pt-BR, pt-PT, ...
url_req = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang='+language

def speech():
	rospy.init_node('gspeech')
        msg = Speech()
        pubm = rospy.Publisher('spoken_line', Speech)

	os.system(cmd1)
	req = urllib2.Request(url_req, data=recording.flac, headers={'Content-type': 'audio/x-flac; rate=16000'})

	try:
		ret = urllib2.urlopen(req)
	except urllib2.URLError:
		# print ROS_ERROR and carry on
		rospy.logerror('Could not transcribe spoken line')

	text = json.loads(ret.read())['hypotheses'][0]['utterance']
	print text

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
		speech()
	except rospy.ROSInterruptException: pass
	except KeyboardInterrupt:
		sys.exit(1)   
