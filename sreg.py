import numpy as num
import pandas as pd
import pysal as ps
from scipy import stats
import statsmodels.api as sm
import seaborn as sns
from sklearn.decomposition import PCA
import statsmodels.formula.api as smf
from sklearn import decomposition
import sklearn.decomposition
from scipy import stats
import patsy as pt
import time

db=pd.read_csv('assault_att.csv')
ds_name='assault_att.csv'
db=db.apply(pd.to_numeric, errors='ignore')

 ########## Independent Variables ########## 
ss = ['HC01_VC112DP03','HC01_VC125DP04','HC01_VC90DP02','HC01_VC08DP03','HC01_VC82DP04','HC01_VC20DP03','HD01_S182','HD01_S171','HD01_S026']

indep=db[ss].as_matrix()
x_names=ss*1

 ########## Dependent Variables ########## 
crime=(db['Count_']).as_matrix().reshape(len(db),1)

 ########## Weight Matrix ########## 
ww = ps.open("crimeR.gal")
w = ww.read()
ww.close()
w_name="crimeR.gal"

 ########## OLS Model ########## 
OLSreg = ps.spreg.OLS(crime,indep)
#b estimation
#the first: intercept
#print 'b, w estimations'
#print OLSreg.betas

print 'OLS Tests'

#T statistics
#null hypothesis: the effect of the regression coefficient is equal to 0. 
print 'T test'
print ps.spreg.diagnostics.t_stat(OLSreg)
#adjusted R^2 value, the fit of the model
print 'R square'
print ps.spreg.diagnostics.ar2(OLSreg)
#F statistics
#print 'F test'
#print ps.spreg.diagnostics.f_stat(OLSreg)

#Multicollinearity
if ps.spreg.diagnostics.condition_index(OLSreg) > 100:
	print 'Multicollinearity'
	for m in range(len(ps.spreg.diagnostics.vif(OLSreg))):
		if m!= 0 and ps.spreg.diagnostics.vif(OLSreg)[m][1]<0.05:
			print 'variable '+str(m)+' has the Multicollinearity issue'
#Heteroscedasticity
if ps.spreg.diagnostics.white(OLSreg)['pvalue']<0.05:
	print 'heteroscedasticity issue based on white statistics'
if ps.spreg.diagnostics.breusch_pagan(OLSreg)['pvalue']<0.05:
	print 'heteroscedasticity issue based on breusch_pagan test'
if ps.spreg.diagnostics.koenker_bassett(OLSreg)['pvalue']<0.05:
	print 'heteroscedasticity issue based on koenker_bassett test'

withcity=[]
outcity=[]
for m in range(len(db['city'])):
	if db['city'][m] == 1:
		withcity.append(float(OLSreg.u[m]))
	else:
		outcity.append(float(OLSreg.u[m]))
if len(stats.levene(num.array(withcity),num.array(outcity)))>1 and stats.levene(num.array(withcity),num.array(outcity))[1]<0.05:
	print 'heteroscedasticity issue based on city boundary'

withrural=[]
outrural=[]
for m in range(len(db['D005'])):
	if db['D005'][m] != 0:
		withrural.append(float(OLSreg.u[m]))
	else:
		outrural.append(float(OLSreg.u[m]))
if len(stats.levene(num.array(withcity),num.array(outcity)))>1 and stats.levene(num.array(withcity),num.array(outcity))[1]<0.05:
	print 'heteroscedasticity issue based on the urban/ rural division'

#Spatial Model
if ps.spreg.diagnostics_sp.MoranRes(OLSreg, w, z=True).p_norm<0.05:
	print 'residuals are spatial autocorrelations'
if ps.Moran(OLSreg.u, w).p_norm < 0.05:
	print 'residuals are spatial autocorrelations'

#Model Choice
if (ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lme[1] <0.01 and ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lml[1]<0.01):
	if (ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlme[1]<0.01 and ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlml[1]<0.01):
		print 'choose any model'
	elif (ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlme[1]>0.01 and ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlml[1]<0.01):
		print 'choose spatial lag model'
	elif (ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlme[1]<0.01 and ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlml[1]>0.01):
		print 'choose spatial error model'
	else:
		print 'spatial error and spatial lag models do not work'

elif (ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lme[1] > 0.01 and ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lml[1]<0.01):
	print 'choose spatial lag model'
elif (ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lme[1] <0.01 and ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lml[1]< 0.01):
	print 'choose spatial error model'
else:
	print 'spatial error and spatial lag models do not work'

#Normality
if ps.spreg.diagnostics.jarque_bera(OLSreg)['pvalue'] < 0.05:
	print 'residuals are not normality distributed'
if len(stats.shapiro(OLSreg.u))>1 and stats.shapiro(OLSreg.u)[1]<0.05:
	print 'residuals are not normality distributed'

 ########## SAR Model ########## 
mllag = ps.spreg.ML_Lag(crime,indep,w,name_y='crime',name_x=x_names,name_w=w_name,name_ds=ds_name) 

print '                                     '
print 'Spatial Lag Tests'
#T statistics
#null hypothesis: the effect of the regression coefficient is equal to 0. 
print 'T test'
print ps.spreg.diagnostics.t_stat(mllag)
#adjusted R^2 value, the fit of the model
print 'R square'
print ps.spreg.diagnostics.ar2(mllag)
#F statistics
#print 'F test'
#print ps.spreg.diagnostics.f_stat(mllag)

#Multicollinearity
for m in range(len(ps.spreg.diagnostics.vif(mllag))):
	if m!= 0 and ps.spreg.diagnostics.vif(mllag)[m][1]<0.05:
		print 'variable '+str(m)+' has the Multicollinearity issue'

#Heteroscedasticity
if ps.spreg.diagnostics.breusch_pagan(mllag)['pvalue']<0.05:
	print 'heteroscedasticity issue based on breusch_pagan test'
if ps.spreg.diagnostics.koenker_bassett(mllag)['pvalue']<0.05:
	print 'heteroscedasticity issue based on koenker_bassett test'

withcity=[]
outcity=[]
for m in range(len(db['city'])):
	if db['city'][m] == 1:
		withcity.append(float(mllag.u[m]))
	else:
		outcity.append(float(mllag.u[m]))
if len(stats.levene(num.array(withcity),num.array(outcity)))>1 and stats.levene(num.array(withcity),num.array(outcity))[1]<0.05:
	print 'heteroscedasticity issue based on city boundary'

withrural=[]
outrural=[]
for m in range(len(db['D005'])):
	if db['D005'][m] != 0:
		withrural.append(float(mllag.u[m]))
	else:
		outrural.append(float(mllag.u[m]))
if len(stats.levene(num.array(withcity),num.array(outcity)))>1 and stats.levene(num.array(withcity),num.array(outcity))[1]<0.05:
	print 'heteroscedasticity issue based on the urban/ rural division'

#Spatial Model
if ps.Moran(mllag.u, w).p_norm < 0.05:
	print 'residuals are spatial autocorrelations'

#Normality
if ps.spreg.diagnostics.jarque_bera(mllag)['pvalue'] < 0.05:
	print 'residuals are not normality distributed'
if len(stats.shapiro(mllag.u))>1 and stats.shapiro(mllag.u)[1]<0.05:
	print 'residuals are not normality distributed'

 ########## AR Model ########## 
mlerror = ps.spreg.ML_Error(crime,indep,w,name_y='crime',name_x=x_names,name_w=w_name,name_ds=ds_name) 

print '                                     '
print 'Spatial Error Tests'
#T statistics
#null hypothesis: the effect of the regression coefficient is equal to 0. 
print 'T test'
print ps.spreg.diagnostics.t_stat(mlerror)
#adjusted R^2 value, the fit of the model
print 'R square'
print ps.spreg.diagnostics.ar2(mlerror)
#F statistics
#print 'F test'
#print ps.spreg.diagnostics.f_stat(mlerror)

#Multicollinearity
for m in range(len(ps.spreg.diagnostics.vif(mlerror))):
	if m!= 0 and ps.spreg.diagnostics.vif(mlerror)[m][1]<0.05:
		print 'variable '+str(m)+' has the Multicollinearity issue'

#Heteroscedasticity
if ps.spreg.diagnostics.breusch_pagan(mlerror)['pvalue']<0.05:
	print 'heteroscedasticity issue based on breusch_pagan test'
if ps.spreg.diagnostics.koenker_bassett(mlerror)['pvalue']<0.05:
	print 'heteroscedasticity issue based on koenker_bassett test'

withcity=[]
outcity=[]
for m in range(len(db['city'])):
	if db['city'][m] == 1:
		withcity.append(float(mlerror.u[m]))
	else:
		outcity.append(float(mlerror.u[m]))
if len(stats.levene(num.array(withcity),num.array(outcity)))>1 and stats.levene(num.array(withcity),num.array(outcity))[1]<0.05:
	print 'heteroscedasticity issue based on city boundary'

withrural=[]
outrural=[]
for m in range(len(db['D005'])):
	if db['D005'][m] != 0:
		withrural.append(float(mlerror.u[m]))
	else:
		outrural.append(float(mlerror.u[m]))
if len(stats.levene(num.array(withcity),num.array(outcity)))>1 and stats.levene(num.array(withcity),num.array(outcity))[1]<0.05:
	print 'heteroscedasticity issue based on the urban/ rural division'

#Spatial Model
if ps.Moran(mlerror.u, w).p_norm < 0.05:
	print 'residuals are spatial autocorrelations'

#Normality
if ps.spreg.diagnostics.jarque_bera(mlerror)['pvalue'] < 0.05:
	print 'residuals are not normality distributed'
if len(stats.shapiro(mlerror.u))>1 and stats.shapiro(mlerror.u)[1]<0.05:
	print 'residuals are not normality distributed'

