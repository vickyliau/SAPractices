import numpy as num
import numpy as np
import pysal
from osgeo import gdal  
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
from osgeo import ogr
import pandas as pd
from pylab import *
import itertools
from scipy.spatial.distance import pdist, squareform

db= pysal.open('gridRan1P.dbf', 'r')
d = {col: db.by_col(col) for col in db.header}
table1=pd.DataFrame(d).fillna(0)
a=num.array(table1['Att'])

#Semi-Variogram
myX=num.array(table1['POINT_X'])
myY=num.array(table1['POINT_Y'])
xycoors=num.array([(i,j) for i, j in zip(myX, myY) ])
xydist=squareform(pdist(xycoors)) #distance of any two points

lag=5
n=len(table1)

myrange=num.array(range(0,int(num.max(xydist))+3*lag,lag))

semi=[]
for h in myrange:
	ssemi=[]
	for i in range(len(xydist)):
		for j in range(i+1,len(xydist)):
			if(xydist[i][j] >= h-lag )and( xydist[i][j] <= h+lag ):
				ssemi.append((a[i]-a[j])*(a[i]-a[j]))
				#print a[i]
				#print a[j]
	semivalue=num.sum(ssemi)/(2*len(ssemi))	
	semi.append(semivalue)
	#print num.sum(ssemi)/(2*len(ssemi))
semivalue=num.array([ [ myrange[m], semi[m] ] for m in range( len( myrange ) ) if semi[m] > 0 ]).T

#Validated by geostatsmodels at https://github.com/cjohnson318/geostatsmodels
P = num.array( table1[['POINT_X','POINT_Y','Att']] )
pw = utilities.pairwise(P)
tolerance = 5
lags = num.arange( tolerance, int(num.max(xydist))+3*lag, tolerance*2)
sill = num.var(P[:,2])

geoplot.semivariogram( P, lags, tolerance )
