import numpy as num
import pandas as pd
import pysal as ps

#stepwise: based on https://onlinecourses.science.psu.edu/stat501/node/329
indepEV1=num.concatenate([indepEV,crime],axis=1)
indepEV1=sm.add_constant(indepEV1, prepend=False)
dbEV=pd.DataFrame(indepEV1)
dbEV.columns=chun+['EV'+str(m) for m in range(EV.shape[1]+1)[1:]]+['crime','constant']
a=dbEV.corr().sort_values(['crime'], ascending=[0])['crime']
crimecorr=a.drop(a.index[0]).drop(a.index[-1]) #the index is the stepwise order

con=num.array([1]*len(dbEV))
cc=sm.add_constant(indep, prepend=False)
time1=time.time()
cmodel = sm.GLM(crime, cc, family=sm.families.Poisson()).fit()

myorder=list(crimecorr.index)
con='constant'
while len(myorder) > 0:
	dd=[]
	for n in range(len(myorder)+2)[2:][:50]:
		#get variables, which reject the null hypothesis
		resign=[]
		recol=[]
		try:
			for e in delindex:
				dd.append(delindex)
			n=n-len(dd)
		except:
			pass
		#print n
		for m in myorder:
			formula='crime ~ '+str(con)+' + '+str(m)
			mod1 = smf.glm(formula=formula, data=dbEV, family=sm.families.Poisson()).fit()
			TAIC=mod1.pvalues[n]
			if TAIC<0.05:
				resign.append(TAIC)
				recol.append(m)
		tab=pd.DataFrame({})
		tab['col']=recol
		tab['sign']=resign
		a=tab.sort_values(['sign'], ascending=[1]).reset_index(drop=True) #variable list in order
		myorder=num.array(a.drop(a.index[0])['col'])
	
		#whether the new enter result in insignificant result -> delete previous elements
		formula1='crime ~ '+str(con)+' + '+str(a['col'][0])
		remod1 = smf.glm(formula=formula1, data=dbEV, family=sm.families.Poisson()).fit()
		delindex=[]
		for p, q in zip(remod1.pvalues,range(len(remod1.pvalues))):
			if p > 0.05:
				delindex.append(remod1.pvalues.index[q])
		#print delindex
		
		myorder=num.delete(myorder, [e for e in range(len(myorder)) if myorder[e] in delindex])
		con=str(con)+' + '+str(a['col'][0])
		for e in delindex:
			rep=e+' + '
			con=con.replace(rep,'')
		#print con
		#print myorder
		if len(myorder)==0:
			break
