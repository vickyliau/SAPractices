import numpy as num
import pysal as ps
import statsmodels.api as sm
num.set_printoptions(suppress=True)

db =  ps.open('tracts_burglary2.dbf','r')
ds_name = "tracts_burglary2.dbf"
y_name = "Count_"
y = (num.array(db.by_col(y_name))/num.array(db.by_col('Shape_Area'))).T
y.shape = (len(y),1)
x_names = ["male5","male5_9","male10_14","male15_19","male20_24","male25_29","male30_34","male35_39","male40_44","male45_49","male50_54","male55_59","male60_64","male65_69","raceL","raceB"]
x = (num.array([db.by_col(var) for var in x_names])/(num.array(db.by_col('Shape_Area')))).T
ww = ps.open("tracts_burglary2_rook.gal")
w = ww.read()
ww.close()
w_name = "tracts_burglary1_rook.gal"
w.transform = 'r'

##########OLS##########
print 'OLS'
OLSreg = ps.spreg.OLS(y,x)
#b estimation
#the first: intercept; the last one: weight parameter
print 'b, w estimations'+str(num.round(OLSreg.betas,10))

# multicollinearity condition index
#less than 100 -> no multi-collinearity; 100 - 1000 -> moderate multi-collinearity; over 1000 -> serious collinearity
print ' multicollinearity condition index'+str(ps.spreg.diagnostics.condition_index(OLSreg))

#White test to check for heteroscedasticity
print 'White test'+str(ps.spreg.diagnostics.white(OLSreg))

#Lagrange Multiplier tests: LM error test
print 'Lagrange Multiplier tests: LM error test'+str(ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lme)

#Lagrange Multiplier tests: Robust LM error test
print 'Lagrange Multiplier tests: Robust LM error test'+str(ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlme)

#Lagrange Multiplier tests: LM lag test
print 'Lagrange Multiplier tests: LM error test'+str(ps.spreg.diagnostics_sp.LMtests(OLSreg, w).lml)

#Lagrange Multiplier tests: Robust LM lag test
print 'Lagrange Multiplier tests: Robust LM error test'+str(ps.spreg.diagnostics_sp.LMtests(OLSreg, w).rlme)

#Moran’s I for spatial autocorrelation in residuals 
print "Morans I"+str([ps.spreg.diagnostics_sp.MoranRes(OLSreg, w, z=True).I,ps.spreg.diagnostics_sp.MoranRes(OLSreg, w, z=True).p_norm])

#Akaike information criterion by the quality of each model between the goodness of fit and the complexity of each model
print 'AIC'+str(num.round(OLSreg.aic,4))

#Schwarz criterion (Bayesian information criterion) by the liklihood function
print 'BIC'+str(num.round(OLSreg.schwarz,4))

#F statistics
print 'F test'+str(ps.spreg.diagnostics.f_stat(OLSreg))

#T statistics
print 'T test'+str(ps.spreg.diagnostics.t_stat(OLSreg))

#adjusted R^2 value, the fit of the model
print 'R square'+str(ps.spreg.diagnostics.ar2(OLSreg))

#standard error of the regression coefficients
print 'standard error'+str(ps.spreg.diagnostics.se_betas(OLSreg))

#log-likelihood value for the regression
print 'log-likelihood value'+str(ps.spreg.diagnostics.log_likelihood(OLSreg))

#Jarque-Bera test for normality in the residuals: a goodness-of-fit test of whether sample data have the skewness and kurtosis matching a normal distribution
#null hypothesis: a joint hypothesis of the skewness is zero and the excess kurtosis is zero
print 'Jarque-Bera test'+str(ps.spreg.diagnostics.jarque_bera(OLSreg))

#Breusch-Pagan test statistic to check for heteroscedasticity: test for heteroskedasticity in a linear regression model
#null hypothesis: homoskedasticity
print 'Breusch-Pagan test statistic'+str(ps.spreg.diagnostics.breusch_pagan(OLSreg))

#Koenker-Bassett test statistic to check for heteroscedasticity
#null hypothesis: homoskedasticity
print 'Koenker-Bassett test statistic'+str(ps.spreg.diagnostics.koenker_bassett(OLSreg))

#variance inflation factor for each independent variable
print 'VIF'+str(ps.spreg.diagnostics.vif(OLSreg))

##########AR = spatial lag model##########
print '                         '
print 'Spatial Lag Model'
mllag = ps.spreg.ML_Lag(y,x,w,name_y=y_name,name_x=x_names,name_w=w_name,name_ds=ds_name) 

#b estimation
#the first: intercept; the last one: weight parameter
print 'b, w estimations'+str(num.round(mllag.betas,4))

#residuals
#print num.round(mllag.u,4)

#predicted y values
#print num.round(mllag.predy,4)

#Akaike information criterion by the quality of each model between the goodness of fit and the complexity of each model
print 'AIC'+str(num.round(mllag.aic,4))

#Schwarz criterion (Bayesian information criterion) by the liklihood function
print 'BIC'+str(num.round(mllag.schwarz,4))

#F statistics
print 'F test'+str(ps.spreg.diagnostics.f_stat(mllag))

#T statistics
print 'T test'+str(ps.spreg.diagnostics.t_stat(mllag))

#adjusted R^2 value, the fit of the model
print 'R square'+str(ps.spreg.diagnostics.ar2(mllag))

#standard error of the regression coefficients
print 'standard error'+str(ps.spreg.diagnostics.se_betas(mllag))

#log-likelihood value for the regression
print 'log-likelihood value'+str(ps.spreg.diagnostics.log_likelihood(mllag))

#Jarque-Bera test for normality in the residuals: a goodness-of-fit test of whether sample data have the skewness and kurtosis matching a normal distribution
#null hypothesis: a joint hypothesis of the skewness is zero and the excess kurtosis is zero
print 'Jarque-Bera test'+str(ps.spreg.diagnostics.jarque_bera(mllag))

#Breusch-Pagan test statistic to check for heteroscedasticity: test for heteroskedasticity in a linear regression model
#null hypothesis: homoskedasticity
print 'Breusch-Pagan test statistic'+str(ps.spreg.diagnostics.breusch_pagan(mllag))

#Koenker-Bassett test statistic to check for heteroscedasticity
#null hypothesis: homoskedasticity
print 'Koenker-Bassett test statistic'+str(ps.spreg.diagnostics.koenker_bassett(mllag))

#variance inflation factor for each independent variable
print 'VIF'+str(ps.spreg.diagnostics.vif(mllag))

#Likelihood ratio test statistic #compare two regressions

"""
#####Ord eigenvalue method#####
print '                         '
print 'Spatial Lag Model: Ord eigenvalue method'
mllagE = ps.spreg.ML_Lag(y,x,w,name_y=y_name,name_x=x_names,name_w=w_name,name_ds=ds_name,method='ord')
#b estimation
print 'b, w estimations'+str(num.round(mllagE.betas,4))

#residuals
#print num.round(mllagE.u,4)

#predicted y values
#print num.round(mllagE.predy,4)

#Akaike information criterion
print 'AIC'+str(num.round(mllagE.aic,4))

#Schwarz criterion
print 'BIC'+str(num.round(mllagE.schwarz,4))

#F statistics
print 'F test'+str(ps.spreg.diagnostics.f_stat(mllagE))

#T statistics
print 'T test'+str(ps.spreg.diagnostics.t_stat(mllagE))

#adjusted R^2 value, the fit of the model
print 'R square'+str(ps.spreg.diagnostics.ar2(mllagE))

#standard error of the regression coefficients
print 'standard error'+str(ps.spreg.diagnostics.se_betas(mllagE))

#log-likelihood value for the regression
print 'log-likelihood value'+str(ps.spreg.diagnostics.log_likelihood(mllagE))

#Jarque-Bera test for normality in the residuals: a goodness-of-fit test of whether sample data have the skewness and kurtosis matching a normal distribution
#null hypothesis: a joint hypothesis of the skewness is zero and the excess kurtosis is zero
print 'Jarque-Bera test'+str(ps.spreg.diagnostics.jarque_bera(mllagE))

#Breusch-Pagan test statistic to check for heteroscedasticity: test for heteroskedasticity in a linear regression model
#null hypothesis: homoskedasticity
print 'Breusch-Pagan test statistic'+str(ps.spreg.diagnostics.breusch_pagan(mllagE))

#Koenker-Bassett test statistic to check for heteroscedasticity
#null hypothesis: homoskedasticity
print 'Koenker-Bassett test statistic'+str(ps.spreg.diagnostics.koenker_bassett(mllagE))

#variance inflation factor for each independent variable
print 'VIF'+str(ps.spreg.diagnostics.vif(mllagE))
"""

##########SAR = spatial error model##########
print '                         '
print 'Spatial Error Model'
mlerror = ps.spreg.ML_Error(y,x,w,name_y=y_name,name_x=x_names,name_w=w_name,name_ds=ds_name) 
#b estimation
print 'b, w estimations'+str(num.round(mlerror.betas,4))

#residuals
#print num.round(mlerror.u,4)

#predicted y values
#print num.round(mlerror.predy,4)

#Akaike information criterion
print 'AIC'+str(num.round(mlerror.aic,4))

#Schwarz criterion
print 'BIC'+str(num.round(mlerror.schwarz,4))

#F statistics
print 'F test'+str(ps.spreg.diagnostics.f_stat(mlerror))

#T statistics
print 'T test'+str(ps.spreg.diagnostics.t_stat(mlerror))

#adjusted R^2 value, the fit of the model
print 'R square'+str(ps.spreg.diagnostics.ar2(mlerror))

#standard error of the regression coefficients
print 'standard error'+str(ps.spreg.diagnostics.se_betas(mlerror))

#log-likelihood value for the regression
print 'log-likelihood value'+str(ps.spreg.diagnostics.log_likelihood(mlerror))

#Jarque-Bera test for normality in the residuals: a goodness-of-fit test of whether sample data have the skewness and kurtosis matching a normal distribution
#null hypothesis: a joint hypothesis of the skewness is zero and the excess kurtosis is zero
print 'Jarque-Bera test'+str(ps.spreg.diagnostics.jarque_bera(mlerror))

#Breusch-Pagan test statistic to check for heteroscedasticity: test for heteroskedasticity in a linear regression model
#null hypothesis: homoskedasticity
print 'Breusch-Pagan test statistic'+str(ps.spreg.diagnostics.breusch_pagan(mlerror))

#Koenker-Bassett test statistic to check for heteroscedasticity
#null hypothesis: homoskedasticity
print 'Koenker-Bassett test statistic'+str(ps.spreg.diagnostics.koenker_bassett(mlerror))

#variance inflation factor for each independent variable
print 'VIF'+str(ps.spreg.diagnostics.vif(mlerror))
"""
#####Ord eigenvalue method#####
print '                         '
print 'Spatial Error Model: Ord eigenvalue method'
mlerrorE = ps.spreg.ML_Error(y,x,w,name_y=y_name,name_x=x_names,name_w=w_name,name_ds=ds_name,method='ord')
#b estimation
print 'b, w estimations'+str(num.round(mlerrorE.betas,4))

#residuals
#print num.round(mlerrorE.u,4)

#predicted y values
#print num.round(mlerrorE.predy,4)

#Akaike information criterion
print 'AIC'+str(num.round(mlerrorE.aic,4))

#Schwarz criterion
print 'BIC'+str(num.round(mlerrorE.schwarz,4))

#####sparse matrix decomposition#####
print '                         '
print 'Spatial Error Model: sparse matrix decomposition'
mlerrorS = ps.spreg.ML_Error(y,x,w,name_y=y_name,name_x=x_names,name_w=w_name,name_ds=ds_name,method='LU')
#b estimation
print 'b, w estimations'+str(num.round(mlerrorS.betas,4))

#residuals
#print num.round(mlerrorS.u,4)

#predicted y values
#print num.round(mlerrorS.predy,4)

#Akaike information criterion
print 'AIC'+str(num.round(mlerrorS.aic,4))

#Schwarz criterion
print 'BIC'+str(num.round(mlerrorS.schwarz,4))
"""

##########ESF model##########
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

ESF = sm.GLM(data.endog, num.append(data.exog, EV), family=sm.families.Poisson()) #Y: data.endog; X variables: data.exog
ESF_results = Poisson_model.fit()

#stepwise

