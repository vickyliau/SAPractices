import numpy as num
import pysal
num.set_printoptions(suppress=True)

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

M=num.eye(fline)-num.ones(fline)/fline
MBM=num.dot(M,weights).dot(M)
evals,evec=num.linalg.eigh(MBM)
evec=evec.T[::-1]
evals=evals[::-1]
sel = evals/evals[0]>0.25
EV=[evec[m] for m in range(len(evals)) if sel[m]==1]

EV=num.array(EV)
