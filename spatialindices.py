import numpy as num
import pysal
from osgeo import gdal  
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
from osgeo import ogr
import pandas as pd

#Moran's I and Geary's C
db= pysal.open('gridRan1P.dbf', 'r')
d = {col: db.by_col(col) for col in db.header}
table1=pd.DataFrame(d).fillna(0)
a=num.array(table1['Att'])

myfile='gridRanQ.gal'
f=open(myfile,'r')
fline=int(f.readline().replace('\n','').split(' ')[1])
lines=[]
for line in f:
	lines.append(line.replace('\n',''))

weights=num.zeros((fline,fline))

n=len(a)
sumw=num.sum(weights)
ymean=num.mean(a)
yvar=sum(abs(a - a.mean())**2)
diff=num.array([(i-j)*(i-j) for i in a for j in a]).reshape(n,n)
meandiff=num.array([(i-ymean)*(j-ymean) for i in a for j in a]).reshape(n,n)

GR=(n-1)*num.sum(weights*diff)/(2*(yvar)*sumw)
MR=num.sum(weights*meandiff)/((yvar/n)*sumw)
print 'mycode on MR: '+str(MR)
print 'mycode on GC: '+str(GR)

#validate by pysal
f = pysal.open('gridRan1.dbf')
y = num.array(f.by_col['Id'])
w = pysal.open('gridRanQ.gal').read()
mi = pysal.Moran(y, w, two_tailed=False)
print 'PySAL code on MR: '+str(mi.I)

gc = pysal.Geary(y, w)
print 'PySAL code on GC: '+str(gc.C)

