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
sel = evals/evals[0]>0.25
EV=[]
for m in range(evec.shape[1]):
	EV.append([evec[m][n] for n in range(len(sel)) if sel[n] == 1])

#P1:	all of the eigenvalues and eigenvectors of a real symmetric matrix consist of real (rather than complex or imaginary) numbers
#P2:	the eigenvalues of a matrix and its transpose are the same
evalM = num.diag(evals)
print evalM == evalM.T

#P3:	the sum of the eigenvalues of a matrix equals the sum of that matrix's principal diagonal elements (i.e., its trace)
print num.trace(MBM) == num.trace(MBM)

#P4:	if some constant b is added to each element in the diagonal of a matrix, then b is added to each of the eigenvalues of that matrix, but the matrix's eigenvectors remain unchanged
evals3,evec3=num.linalg.eigh(MBM+3)
print num.round((evals) - evals3,3)
print num.array((evec - evec3), dtype=float)

#P5:	if a matrix is multiplied by some scalar constant, then its eigenvalues also are multiplied by this constant, but its eigenvectors remain unchanged
evals3,evec3=num.linalg.eigh(MBM*3)
print num.round(evals*3 - evals3,3)
print num.round(evec - evec3, 3)

#P6:	the product of a matrix's eigenvalues equals the value of that matrix's determinant
print num.round(evals.prod(),3) == num.round(num.linalg.det(MBM),3)

#P7:	the eigenvalues of a matrix and its inverse are inverses of each other, while the eigenvectors are the same
print num.dot(num.linalg.inv(evalM), evalM) == num.eye(MBM.shape[0])
print num.round(num.dot(num.linalg.inv(evec), evec),0) == num.eye(MBM.shape[0])

#P8:	if a matrix is powered by some positive integer value, each of its eigenvalues is powered by this same positive integer value, but its eigenvectors remain unchanged
evalsP2,evecP2=num.linalg.eigh(num.linalg.matrix_power(MBM,3))
num.round(num.linalg.matrix_power(evalM,3).diagonal(),3) == num.round(evalsP2,3)

#P9:	for a symmetric matrix, two eigenvectors associated with two distinct eigenvalues are mutually orthogonal (i.e., EhTEk = 0, h ? k)
N = 10
b = num.random.randint(0, 20, size=(10,10)) #num.random.uniform(0.,20., size=(10,10))
bs = (b + b.T)/2
evalbs,evecbs=num.linalg.eigh(bs)
print num.round(num.dot(evecbs[0],evecbs[2]),5)

#P10:	for a real symmetric matrix, the transpose of the eigenvector matrix extracted from it equals the inverse of this eigenvector matrix (i.e., ET = E-1) 
print num.linalg.inv(evecbs) == evecbs.T

#P11:	the eigenvalues of a triangular or diagonal matrix are the elements in its principal diagonal
a=num.arange(25).reshape((5,5))
tu = num.triu(a, k=0)
evaltu,evectu=num.linalg.eigh(tu)
tt=[]
for i in evaltu:
	if i in a:
		tt.append(i)
print tt == evaltu

#P12:	the principal (i.e., largest or dominant) eigenvalue of a matrix is contained in that interval defined by the largest and smallest row sums for this matrix, where these sums are of the absolute values of the row cell entries
a=num.arange(25).reshape((5,5))
evala,eveca=num.linalg.eigh(a)
print num.max(evala) < num.max(num.sum(a,axis=1)) and num.max(evala) > num.min(num.sum(a,axis=1))

#P13:	the principal eigenvector of a nonnegative, symmetric matrix has all nonnegative values.
P = np.array([[2, 1, 0], [1, 1, 5], [0, 5, 3]])
D, V = linalg.eig(P)
V=V.T
print num.array([i for i in V[num.where(D==num.max(D))[0][0]] if i > 0]) == V[num.where(D==num.max(D))[0][0]]

#P14:	the principal eigenvalue of a matrix is positive, and no other eigenvalue of this matrix is greater in absolute value
print num.around(num.array([i for i in evals if num.max(evals) > abs(i)]),3) == num.around(num.delete(evals,num.where(evals==num.max(evals))[0][0]),3)

#P15:	the sum of the squared eigenvalues of a matrix is less than or equal to the sum of all of the elements of this matrix, where these sums are of the absolute values of the cell entries, with exact equality achieved for binary matrices
print num.sum(num.array([i*i for i in evals])) < num.sum(num.absolute(MBM)) or num.sum(num.array([i*i for i in evals])) == num.sum(num.absolute(MBM))

