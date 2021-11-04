import os
import sys
import math
import numpy as np
import time
import os.path

from OMPython import OMCSessionZMQ

print("building model...")
os.system("rm -f ./System")    

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
print("model built")

p=10
number_test=10

min_T = 1
max_T = 10
delta_T = (max_T - min_T)/(p)

best_T=min_T


total_tests = 0
test_pass=0

inizio=time.time()

array_successi=[]
print("p = ",p)
print("number test = ",number_test)
print("min = ",min_T)
print("max = ",max_T)

#array=[1.0, 1.38, 1.76, 2.14, 2.52, 3.66, 4.8, 6.7, 1.3, 1.9, 2.8, 4.0, 5.5, 6.39]   # USATO PER TESTARE PRECISI T

for i1 in range(0,p,1):
#for par1 in array:

	print("\n\n\nIteration: ",i1)
	#print("\n\n\n Iteration: ", par1)
	
	total_tests=total_tests+1
	num_fail = 0
	num_pass = 0
	par1=min_T + delta_T*i1;
	
	for i2 in range(number_test):

		with open("parameters.txt", "wt") as f:
			f.write("ctr1.T="+str(par1)+"\n")
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
	
	
		os.system("./System -s=rungekutta -overrideFile=parameters.txt > log")
		time.sleep(0.2)

		y = omc.sendExpression("val(monitor1.y, 50000.0, \"System_res.mat\")")
		y2 = omc.sendExpression("val(monitor2.y, 50000.0, \"System_res.mat\")")
		
	
		#os.system("rm -f System_res.mat")

		if (float(y)<0.5)  and (float(y2)<0.5):
			num_pass=num_pass+1

		else :
			
			
			num_fail=num_fail+1
			with open ("output_synth.txt", 'a') as g:
				g.write("------ERRORE-------"+"\n"+"Valore del monitor1:"+ str(y)+"\n"+"Valore del monitor2:"+ str(y2)+"\n\n")
				g.flush()
				os.fsync(g)
				
				
	
		
				
	if (num_fail==0) :
		array_successi.append(par1)
	
		if (best_T<par1) :
			best_T=par1
			
		test_pass=test_pass+1
		with open ("output_synth.txt", 'a') as g:
			g.write("Feasible: ctr1.T="+str(par1)+"; best-so-far="+str(best_T)+"\n")
			g.flush()
			os.fsync(g)
		
	print("Test per T = ", par1)	
	print("num pass: ", num_pass)
	print("num_fail: ", num_fail)

fine=time.time()
tempo=fine-inizio

print("\nTempo di esecuzione: ", tempo)
print("num feasible = ", test_pass," total tests = ",  total_tests)
print("Best solution: ")
print("T = ", best_T)
print("Array dei T di successo: ",array_successi)


















