#!/usr/bin/python
# try:
#################### import code - begin #################### 
import sys, os, socket, time
os.chdir('/scripts/appleBench/')
sys.path.append('lib')
sys.path.append('libApple')
import dictFunc
import directory
import log
import systemUtil
import userUtil
import timeFunc
import simpleMail
import fileFunctions
import appleSetup
import patches
import blue
import appleDateTime
import sharing
import energy
import security
import logChecks
import network
import access
import sudo
import keychain
import root
import login
import password
import accounts
import file
import apps
import LaRC
import screensaver

# except ImportError:
# 	print "missing modules for main.py"
# 	sys.exit(1)
#################### import code - end #################### 

############### script setup - begin #####################

############## variable assignments - begin #####################
variableAssign="LIST/baseVariables.txt"
baseVar = dictFunc.fileToDict(variableAssign, ",")
	
variableAssign="LIST/variableAssign.txt"
dictVar = dictFunc.fileToDict(variableAssign, "#")
sizeOfBaseDict = len (baseVar)
for x in range(0, sizeOfBaseDict):
	for (n, v) in dictVar.items():
		var = dictVar[n]
		for (key, value) in baseVar.items():
			searchTerm="<"+str(key)+">"
			retVal=var.find(searchTerm)
			if retVal != -1:
				newString = var.replace(searchTerm, value)
				dictVar[n]=newString

for (n, v) in dictVar.items():
	exec('%s=%s' % (n, repr(v)))

hostName=socket.gethostname()
cssDir=hostName+".ndc.nasa.gov/repository/"

logCount = directory.countFilesWithPrefix (baseLog,"log_")
mailList = {}
from_addr = "ladmin@" + hostName
mailList['from_addr'] = from_addr
mailList['to_addr'] = to_addr
message = ""
start_time = time.time()

############## variable assignments - end #####################

l=log.log()
l.setData(prefix, "myLogger")
l.logDelete("LOG",logCount,logNum)
logNameFile = l.logName()
l.info("logNameFile: " + logNameFile)
l.info("log count: " + str(logCount))
l.info("start_time: " + str(start_time))
#if file does not exist =>  used to avoid double running the script
retDict=systemUtil.createRaceConditionFile(checkfile)
retVal=int(retDict['retVal'])
comment=retDict['comment']
if retVal == 1:
	mailList['subject'] = "double run script fault - " + scriptNameMail + ":  --- " + checkfile +" exists ---"
	message = "double run script fault - " + scriptNameMail  + ":  --- "+ checkfile + " exists --- \n"
	message = message + comment
	l.abort(message)
	mailList['message'] = message
	shortMessage (mailList)
	sys.exit(1)
	
userName=userUtil.getUsername()
l.info ("user name: " + userName)	
total = len(sys.argv)
if total == 2:
	stage=str(sys.argv[1])
	#default production
	#developement
	l.info ("First argument: %s" % str(sys.argv[1]))
else:
	stage="production"
############################# main - begin ###########################

if stage == "production":
	l.info("production")
	appleSetup.run(l, TEMP)
	patches.run(l, TEMP)
 	blue.run(l)
 	appleDateTime.run(l, TEMP, timeserver)
 	screensaver.run(l, TEMP, dictVar)
# 	sharing.run(l, TEMP)
# 	energy.run(l, TEMP)
# 	security.run(l, TEMP)
# 	logChecks.run(l, TEMP)
# 	network.run(l, TEMP)
# 	access.run (l, TEMP)
# 	sudo.run (l, TEMP)
# 	keychain.run (l, TEMP)
# 	root.run (l, TEMP)
# 	login.run (l, TEMP)
# 	password.run (l, TEMP)
# 	accounts.run (l, TEMP)
# 	file.run (l, TEMP)
# 	apps.run (l, TEMP)
# 	LaRC.run (l, TEMP)	
	
elif stage == "development":
	l.info("development")	
else:
	l.info("other")
############################# main - end ###########################

end_time = time.time()
timeDict = timeFunc.timeDuration (end_time, start_time)
printHours = timeDict['printHours']
printMins = timeDict['printMins']
printSec = timeDict['seconds']
logBody = l.logfileAsString()
body = scriptName +" script on " + hostName + " took " + str(printHours) + ":" + str(printMins) + " or " + str(printSec) + " seconds to run"
subject = hostName + " " + scriptNameMail
mailList['message'] = logBody + body
mailList['subject'] = subject
simpleMail.shortMessage (mailList)
fileFunctions.fileDelete(checkfile)

