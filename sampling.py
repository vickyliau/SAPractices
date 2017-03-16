from __future__ import division
import numpy as num
import fiona
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.geometry import shape
import glob
from osgeo import ogr, gdal, osr

PP=glob.glob('*P.shp')
poly=glob.glob('*1.shp')
n=30
num.random.seed(n*n)

#population
for p in range(len(PP)):
	points=[]
	for pol1 in fiona.open(PP[p]):
		points.append(shape(pol1['geometry']))

	polys=[]
	crimeC=[]
	for pol in fiona.open(poly[p]):
		polys.append(Polygon(shape(pol['geometry'])))
		crimeC.append(pol['properties']['Count_'])

	polysb=fiona.open(poly[p]).bounds #(minx, miny, maxx, maxy)
	
	print 'Population'+str(num.mean(crimeC))+' '+str(poly[p].replace('counts1.shp',''))
	print 'Population'+str(num.var(crimeC))+' '+str(poly[p].replace('counts1.shp',''))

	#random sample: randomly sample n pairs of coordinates
	rsx=num.random.uniform(polysb[0],polysb[2],n)
	rsy=num.random.uniform(polysb[1],polysb[3],n)
	rs=[]
	for i in range(len(rsx)):
		rs.append(Point(rsx[i],rsy[i]))
	ccrs=[]
	for i in rs:
		for j in range(len(polys)):
			if i.within(polys[j]):
				ccrs.append(crimeC[j])

	estmeanrs=num.mean(num.array(ccrs))
	estvarrs=num.var(num.array(ccrs))
	print 'Random Sample'+str(estmeanrs)+' '+str(poly[p].replace('counts1.shp',''))
	print 'Random Sample'+str(estvarrs)+' '+str(poly[p].replace('counts1.shp',''))
	"""
	if p==0:
		spatialReference = osr.SpatialReference()
		spatialReference.ImportFromProj4('+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs')
		driver = ogr.GetDriverByName('Esri Shapefile')
		ds = driver.CreateDataSource('rs30.shp')
		layer = ds.CreateLayer('', spatialReference, geom_type=ogr.wkbPoint)
		# Add one attribute
		layer.CreateField(ogr.FieldDefn('crime', ogr.OFTInteger))
		defn = layer.GetLayerDefn()
		for j, k in zip(rs, ccrs):
			feat = ogr.Feature(defn)
			feat.SetField('crime', k)

			geom = ogr.CreateGeometryFromWkb(j.wkb)
			feat.SetGeometry(geom)
			layer.CreateFeature(feat)
		feat = geom = None  # destroy these
	"""

	#systematic sample: along with grids, randomly sample a single pair of coordinates
	xr=(polysb[2]-polysb[0])/6
	yr=(polysb[3]-polysb[1])/7

	sysx=num.random.uniform(polysb[0],polysb[2],1)
	sysy=num.random.uniform(polysb[1],polysb[3],1)
	sxrange=num.arange(int(polysb[0]), int(polysb[0])+int(xr)*6,int(xr))
	sxrangen=num.arange(int(polysb[0])-int(xr)*6, int(polysb[0]),int(xr))
	ssx=num.append(sxrange,sxrangen)
	syrange=num.arange(int(polysb[1]), int(polysb[1])+int(yr)*7,int(yr))
	syrangen=num.arange(int(polysb[1])-int(yr)*7, int(polysb[1]),int(yr))
	ssy=num.append(syrange,syrangen)
	syss=[]
	for i in ssx:
		if i > polysb[0] and i <polysb[2]:
			for j in ssy:
				if j>polysb[1] and j<polysb[3]:

					syss.append(Point(i, j))

	sypoly=[]
	for i in syss:
		for j in range(len(polys)):
			if i.within(polys[j]):
				sypoly.append(crimeC[j])
	estmeansy=num.mean(num.array(sypoly))
	estvarsy=num.var(num.array(sypoly))
	print 'Systematic Sample'+str(estmeansy)+' '+str(poly[p].replace('counts1.shp',''))
	print 'Systematic Sample'+str(estvarsy)+' '+str(poly[p].replace('counts1.shp',''))
	"""
	if p==0:
		spatialReference = osr.SpatialReference()
		spatialReference.ImportFromProj4('+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs')
		driver = ogr.GetDriverByName('Esri Shapefile')
		ds = driver.CreateDataSource('sys30.shp')
		layer = ds.CreateLayer('', spatialReference, geom_type=ogr.wkbPoint)
		# Add one attribute
		layer.CreateField(ogr.FieldDefn('crime', ogr.OFTInteger))
		defn = layer.GetLayerDefn()
		for j, k in zip(syss, sypoly):
			feat = ogr.Feature(defn)
			feat.SetField('crime', k)

			geom = ogr.CreateGeometryFromWkb(j.wkb)
			feat.SetGeometry(geom)
			layer.CreateFeature(feat)
		feat = geom = None  # destroy these
	"""

	#cluster sample: within each polygon, randomly sample a single pair of coordinates
	m=int(num.random.randint(1,len(polys), size=1))
	clu=polys[m-1].bounds
	estmeanC=crimeC[m-1]
	estvarC=0
	clux=num.random.uniform(clu[0],clu[2],30)
	cluy=num.random.uniform(clu[1],clu[3],30)
	clus=[]
	while True:
		#print '1'
		clux=num.random.uniform(clu[0],clu[2],1)[0]
		cluy=num.random.uniform(clu[1],clu[3],1)[0]
		if Point(clux, cluy).within(polys[m-1]) == True:
			clus.append(Point(clux, cluy))		
			if len(clus) == 30:
				break
	print 'Cluster Sample'+str(estmeanC)+' '+str(poly[p].replace('counts1.shp',''))
	print 'Cluster Sample'+str(estvarC)+' '+str(poly[p].replace('counts1.shp',''))
	"""
	if p ==0:
		spatialReference = osr.SpatialReference()
		spatialReference.ImportFromProj4('+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs')
		driver = ogr.GetDriverByName('Esri Shapefile')
		ds = driver.CreateDataSource('clus30.shp')
		layer = ds.CreateLayer('', spatialReference, geom_type=ogr.wkbPoint)
		# Add one attribute
		layer.CreateField(ogr.FieldDefn('crime', ogr.OFTInteger))
		defn = layer.GetLayerDefn()
		for j, k in zip(clus, [int(crimeC[m-1])]*len(clus)):
			feat = ogr.Feature(defn)
			feat.SetField('crime', k)

			geom = ogr.CreateGeometryFromWkb(j.wkb)
			feat.SetGeometry(geom)
			layer.CreateFeature(feat)
		feat = geom = None  # destroy these
	"""

	#stratified sample: randomly sample on a single polygon
	s=num.random.randint(1,len(polys), size=30)
		
	strc=[]
	strp=[]
	for i in s:
		ss=polys[i-1].bounds #boundary of each polygon
		strp1=[]
		while True:
			#print '1'
			ssx=num.random.uniform(ss[0],ss[2],1)[0]
			ssy=num.random.uniform(ss[1],ss[3],1)[0]
			if Point(ssx, ssy).within(polys[i-1]) == True:
				strp1.append(Point(ssx, ssy))		
				if len(strp1) == 1:
					break
		strp.append(strp1[0])
		#print strp
		strc.append(crimeC[i-1])
	
	estmeanstr=num.mean(num.array(strc))
	estvarstr=num.var(num.array(strc))
	print 'Stratified Sample'+str(estmeanstr)+' '+str(poly[p].replace('counts1.shp',''))
	print 'Stratified Sample'+str(estvarstr)+' '+str(poly[p].replace('counts1.shp',''))
	"""
	if p == 0:
		spatialReference = osr.SpatialReference()
		spatialReference.ImportFromProj4('+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs')
		driver = ogr.GetDriverByName('Esri Shapefile')
		ds = driver.CreateDataSource('str30.shp')
		layer = ds.CreateLayer('', spatialReference, geom_type=ogr.wkbPoint)
		# Add one attribute
		layer.CreateField(ogr.FieldDefn('crime', ogr.OFTInteger))
		defn = layer.GetLayerDefn()
		for j, k in zip(strp, strc):
			feat = ogr.Feature(defn)
			feat.SetField('crime', k)

			geom = ogr.CreateGeometryFromWkb(j.wkb)
			feat.SetGeometry(geom)
			layer.CreateFeature(feat)
		feat = geom = None  # destroy these
	"""
