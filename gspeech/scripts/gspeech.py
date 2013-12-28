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
from gspeech_msgs.msg import SpeechArray

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
    linesArr = SpeechArray()

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
        
    try:
        json_msg = json.loads(ret.read())
        print json_msg
    except ValueError:
        rospy.loginfo('No JSON object could be decoded')

    # status = 0 means something was recognised
    # it appears that status = 5 means that nothing could be
    # recognised, but sox recording and urllib2 requests worked
    if json_msg['status'] == 0:
        for i in range(0, len(json_msg['hypotheses'])):
            msg.speech = json_msg['hypotheses'][i]['utterance']
            msg.confidence = json_msg['hypotheses'][i]['confidence']
            linesArr.lines = linesArr.lines + [msg]
        linesArr.header.stamp = rospy.Time.now()
        pubm.publish(linesArr)
        #text = json_msg['hypotheses'][0]['utterance']
        #print text
    elif json_msg['status'] == 5:
        rospy.loginfo('Could not transcribe spoken line')
	
    speech()	
	


if __name__ == '__main__':
    try:
        rospy.init_node('gspeech')
        pubm = rospy.Publisher('spoken_line', SpeechArray)
        speech()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        sys.exit(1)
