import subprocess 
import re
import os

memoryProfile = 'Win7SP1x86_23418'
proccessIDList=[]

cwd = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(cwd, "dumpOfExes")):
	os.makedirs(os.path.join(cwd, "dumpOfExes"))
dumpDirectory = os.path.join(cwd, "dumpOfExes")

#thing = subprocess.check_output(['volatility', '-f', 'ch2.dmp', 'imageinfo'])

#thing = subprocess.check_output("ls")

#result = re.search("Suggested Profile\(s\) : ([^\n]*)", thing)
#profile = result.group(0).split(", ")
#profile[0] = re.sub("Suggested Profile\(s\) : ", "", profile[0])
#memoryProfile = profile[0]

#pslist
pslistOutput = subprocess.check_output(['volatility', '-f', 'ch2.dmp', '--profile='+memoryProfile, "pslist"])


pslistOutputParsed = pslistOutput.split()
for indx, value in enumerate(pslistOutputParsed):
	if re.search("(\A[0-9A-Fa-f]x)[0-9A-Fa-f]",value) != None:
		proccessIDList.append(pslistOutputParsed[indx+2])


for PID in proccessIDList:
	ExtractionProcess = subprocess.Popen(['volatility', '-f', 'ch2.dmp', '--profile='+memoryProfile, "--dump-dir="+dumpDirectory,"procdump", "-p "+PID]) 
	ExtractionProcess.wait()
	print("yay")

