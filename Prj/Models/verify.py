import os
import sys
import math
import numpy as np
import time
import os.path

from OMPython import OMCSessionZMQ


print("building model...")

omc = OMCSessionZMQ()
omc.sendExpression("getVersion()")
omc.sendExpression("cd()")

omc.sendExpression("loadModel(Modelica)")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"connectors.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"student.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"gomp_mc.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"controller1.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"controller2.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"aula.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"monitor.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"monitor2.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("loadFile(\"system.mo\")")
omc.sendExpression("getErrorString()")

omc.sendExpression("buildModel(System, stopTime=50000)")
omc.sendExpression("getErrorString()")
print("model built\n")


np.random.seed(1)

num_pass = 0
num_fail = 0
y = 0.0

with open ("log_verify", 'wt') as f:
        f.write("Begin log"+"\n")
        f.flush()
        os.fsync(f)
        
with open ("output_verify.txt", 'wt') as f:
        f.write("Outcomes"+"\n\n")
        f.flush()
        os.fsync(f)
        
inizio=time.time()
array_seeds=[]

for i in range(100):
#        print "Test ", i

    with open ("modelica_rand.in", 'wt') as f:
        rand1 = math.trunc(np.random.uniform(0,200000))
        rand2 = math.trunc(np.random.uniform(0,200000))
        rand3 = math.trunc(np.random.uniform(0,200000))
        rand4 = math.trunc(np.random.uniform(0,200000))
        rand5 = math.trunc(np.random.uniform(0,200000))
        rand6 = math.trunc(np.random.uniform(0,200000))
        rand7 = math.trunc(np.random.uniform(10,200))
        f.write("student.globalSeed="+str(rand1)+"\n")
        f.write("student.localSeed="+str(rand2)+"\n")
        f.write("gomp.globalSeed="+str(rand3)+"\n")
        f.write("gomp.localSeed="+str(rand4)+"\n")
        f.write("aula.globalSeed="+str(rand5)+"\n")
        f.write("aula.localSeed="+str(rand6)+"\n")
        f.write("gomp.max="+str(rand7)+"\n")
        f.flush()
        os.fsync(f)

    with open ("log_verify", 'a') as f:
        f.write("\nTest "+str(i)+" :\n")
        f.flush()
        os.fsync(f)
        
    os.system("./System -overrideFile=modelica_rand.in >> log")
    time.sleep(0.1)         
       # os.system("rm -f modelica_rand.in")   

    y = omc.sendExpression("val(monitor1.y, 50000.0, \"System_res.mat\")")
    y2 = omc.sendExpression("val(monitor2.y, 50000.0, \"System_res.mat\")")
    #y2= omc.sendExpression("val(monitor.errore, 50000.0, \"System_res.mat\")")
    os.system("rm -f System_res.mat")      
    
    
        
    with open ("output_verify.txt", 'a') as g:
        if (y == 0) and (y2==0):
            num_pass = num_pass + 1.0
            g.write("y["+str(i)+"] = "+str(y)+", y2:"+str(y2)+": SUCCESS\n")
        else:
            print("student.globalSeed: ",rand1)
            print("student.localSeed: ",rand2)
            print("gomp.globalSeed: ",rand3)
            print("gomp.localSeed: ",rand4) 
            print("aula.globalSeed: ",rand5)
            print("aula.localSeed: ",rand6) 
            print("gomp.max: ",rand7)    
            print("Monitor1 value at iteration", i, ": ",  y,"\t\terrori totali: ", num_fail,"\n")
            print("Monitor2 value at iteration", i, ": ",  y2,"\t\terrori totali: ", num_fail,"\n")
            #print("Errore: ", y2)
            array_seeds.append([rand1,rand2,rand3,rand4])
            num_fail = num_fail + 1.0
            g.write("y["+str(i)+"] = "+str(y)+", y2:"+str(y2)+": FAIL\n")
            g.flush()
            os.fsync(g)

fine=time.time()
tempo=fine-inizio

print("\nTempo di esecuzione: ", tempo)
print("num pass = ", num_pass)
print("num fail = ", num_fail)
print("total tests = ",  num_pass + num_fail)
print("pass prob = ", num_pass/(num_pass + num_fail))
print("fail prob = ", num_fail/(num_pass + num_fail))

print("\nSeeds che hanno creato problemi: ")
for x in range(len(array_seeds)):
	print(array_seeds[x])



