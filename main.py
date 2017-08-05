#Script to run procdump on all processes in a mem dump

# get args
#output directory
#get memory dump file
#get profile
#get proccess list
#go through process list
#send pid to procdump
#hash all resulting files

import subprocess 
import re
import os

memoryProfile = 'Win7SP1x86_23418'
proccessIDList=[]

cwd = os.path.dirname(os.path.realpath(__file__))
#Create dir to put all the executables we are making
if not os.path.exists(os.path.join(cwd, "dumpOfExes")):
	os.makedirs(os.path.join(cwd, "dumpOfExes"))
dumpDirectory = os.path.join(cwd, "dumpOfExes")

#Get Profile of mem dump
imageInfoOutput = subprocess.check_output(['volatility', '-f', 'ch2.dmp', 'imageinfo'])

profileLine = re.search("Suggested Profile\(s\) : ([^\n]*)", imageInfoOutput)
profile = profileLine.group(0).split(", ")
#can remove?
#profile[0] = re.sub("Suggested Profile\(s\) : ", "", profile[0])
memoryProfile = profile[0]

#pslist
pslistOutput = subprocess.check_output(['volatility', '-f', 'ch2.dmp', '--profile='+memoryProfile, "pslist"])


pslistOutputParsed = pslistOutput.split()
for indx, value in enumerate(pslistOutputParsed):
	if re.search("(\A[0-9A-Fa-f]x)[0-9A-Fa-f]",value) != None:
		proccessIDList.append(pslistOutputParsed[indx+2])

#Call procdump for all PIDs
for PID in proccessIDList:
	ExtractionProcess = subprocess.Popen(['volatility', '-f', 'ch2.dmp', '--profile='+memoryProfile, "--dump-dir="+dumpDirectory,"procdump", "-p "+PID]) 
	ExtractionProcess.wait()


#Hash all the outputed files
def md5Hash(string):
	hash_object = hashlib.md5(string.encode())
	hash_object= hash_object.hexdigest()
	return hash_object

fileHashes = []
for filename in os.listdir(dumpDirectory):
	if filename.endswith(".exe"):
		fileHashes.append(filename)
		fileHashes.append(md5Hash(os.path.join(dumpDirectory,filename)))

#Add row to file if already exists, w+ makes file if no file, and write filename and hash
if os.path.exists(os.path.join(cwd, "outputHashes.txt")):
	print("Output file already exists...adding to the end of the file")
	with open("outputHashes.txt", "a") as outputFile:
		outputFile.write("-"*10)
		outputFile.close()
with open("outputHashes.txt", "w+") as outputFile:
	for filename, hashString in fileHashes:
		outputFile.write(filename + " , " + hashString)