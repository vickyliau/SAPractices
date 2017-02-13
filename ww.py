from __future__ import division
import numpy as num
import pysal

myfile='gridRanQ.gal'
f=open(myfile,'r')
fline=int(f.readline().replace('\n','').split(' ')[1])
lines=[]
for line in f:
	lines.append(line.replace('\n',''))

weights=num.zeros((fline,fline))

for m in range(len(lines)):
	#lines for the observation IDs and the number of neighbors
	obs=int(lines[m-1].split(' ')[0]) #get the observation IDs
	if m%2==1:
		for n in lines[m].split(' '):
			weights[obs-1][int(n)-1]=1

#C weight
#tt=num.array([[0,1,0,0,0,0,0,0,0],[1,0,1,0,0,0,0,0,0],[0,1,0,1,0,0,0,0,0],[0,0,1,0,1,0,0,0,0],[0,0,0,1,0,1,0,0,0],[0,0,0,0,1,0,1,0,0],[0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,1,0]])
evalsC,evecC=num.linalg.eigh(weights)
evalsC1=evecC.T[[i for i in range(len(evalsC)) if evalsC[i] == num.max(evalsC)][0]]


#W weight
weightsW=num.array([weights[i]/num.sum(weights[i]) for i in range(len(weights))])
evalsW,evecW=num.linalg.eigh(weightsW)

#spatial filter
fline=len(evalsC)
M=num.eye(fline)-num.ones(fline)/fline
MBM=num.dot(M,weights).dot(M)
evals,evec=num.linalg.eigh(MBM)

evals1=evec.T[[i for i in range(len(evals)) if evals[i] == num.max(evals)][0]]

