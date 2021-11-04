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

p=200
number_test=10

min_T = 1
max_T = 20
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


array_test= [1.0, 1.095, 1.19, 1.2850000000000001, 1.38, 1.475, 1.57, 1.665, 1.76, 1.855, 1.95, 2.045, 2.14, 2.2350000000000003, 2.33, 2.425, 2.52, 2.615, 2.71, 2.8049999999999997, 2.9, 2.995, 3.09, 3.185, 3.2800000000000002, 3.375, 3.47, 3.565, 3.66, 3.755, 3.85, 3.945, 4.04, 4.135, 4.23, 4.325, 4.42, 4.515000000000001, 4.609999999999999, 4.705, 4.8, 4.895, 4.99, 5.085, 5.18, 5.275, 5.37, 5.465, 5.5600000000000005, 5.75, 5.845, 5.94, 6.035, 6.13, 6.225, 6.415, 6.51, 6.605, 6.7, 6.795, 6.89, 6.985, 7.365, 7.46, 7.65, 7.745, 7.84, 7.9350000000000005, 8.030000000000001, 8.125, 8.219999999999999, 8.315000000000001, 8.41, 8.504999999999999, 8.6, 8.695, 8.79, 9.075, 9.17, 9.265, 9.36, 9.455, 9.55, 9.74, 9.835, 9.93, 10.025, 10.215, 10.405, 10.5, 10.595, 10.69, 10.785, 10.88, 10.975, 11.07, 11.165000000000001, 11.355, 11.45, 11.545, 11.64, 11.735, 11.925, 12.21, 12.495000000000001, 12.78, 13.16, 13.255, 13.35, 13.635, 13.73, 13.825, 14.015, 14.11, 14.205, 14.395, 14.585, 14.68, 14.870000000000001, 14.965, 15.06, 15.25, 15.345, 15.535, 15.63, 15.82, 16.009999999999998, 16.2, 16.295, 16.485, 16.675, 16.77, 16.865000000000002, 16.96, 17.055, 17.15, 17.245, 17.34, 17.435, 17.53, 17.625, 17.72, 17.815, 18.005, 18.48, 18.575, 18.765, 18.955000000000002, 19.05, 19.240000000000002, 19.335, 19.43, 19.525, 19.62, 19.81]


for i1 in array_test:

	print("\n\n\nIteration: ",i1)
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
				g.write("Infeasible: ctr.T="+str(par1)+"; best-so-far="+str(best_T)+"\n")
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


















