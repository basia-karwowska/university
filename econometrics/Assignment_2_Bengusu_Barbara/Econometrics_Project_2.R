# ECONOMETRICS PROJECT 2

## Data set and packages
library(haven)
data_prod <- haven::read_dta("prodfn.dta")

install.packages("plm")
library(plm)
library(lmtest)
## PANEL DATA ESTIMATORS
 

### Between - pooled OLS
POLS<-lm(formula=y~k+l, data=data_prod)
summary(POLS) # R^2 ONLY 0.187

### Within - fixed effects (firm-, no time-specific fixed effects)
FE_firm<-plm(y~k+l, index=c('ivar', 'tvar'), model='within', data=data_prod)
summary(FE_firm) #R^2 is at 0.18
fixef(FE_firm) # level FE
fixef(FE_firm, type="dmean") # demeaned FE
fixef(FE_firm, type="dfirst") # difference from the first element FE

### Within - fixed effects (time- and no firm-specific fixed effects)
FE_time<-plm(y~k+l, index=c('ivar', 'tvar'), effect="time", model='within', data=data_prod)
summary(FE_time) #r^2 0.21
fixef(FE_time) # level FE
fixef(FE_time, type="dmean") # demeaned FE
fixef(FE_time, type="dfirst") # difference from the first element FE


### Within - twoway (both firm- and time-specific fixed effects)
FE_twoway<-plm(y~k+l, index=c('ivar', 'tvar'), effect="twoways", model='within', data=data_prod)
summary(FE_twoway) #r^2 0.21
fixef(FE_twoway, "individual") # level FE
fixef(FE_twoway, "time") # demeaned FE
fixef(FE_twoway, "twoways") # difference from the first element FE

### First difference model
FE_FD=plm(y~k+l, index=c("ivar", "tvar"), model="fd", data=data_prod)
#What is this model?? 

### Random effects (individual)
RE_firm<-plm(y~k+l, index=c('ivar', 'tvar'), model='random', data=data_prod)
summary(RE_firm) #R^2 0.18, rejects chisq which means random effects has a
#Significant contribution. 

### Random effects (time)
RE_time<-plm(y~k+l, index=c('ivar', 'tvar'), effect="time", model='random', data=data_prod)
summary(RE_time) 
#R2 is 0.218, chisquare is rejected

### Random effects (twoway)
RE_twoway<-plm(y~k+l, index=c('ivar', 'tvar'), effect="twoways", model='random', data=data_prod)
summary(RE_twoway)
#R^2 0.218, chisquare is rejected


### HAUSMAN TEST
HS_individual=phtest(FE_firm, RE_firm)
#Fails to reject the null (p-value is 0.9793), both models are consistent.
HS_time=phtest(FE_time, RE_time)
#Fails to reject the null, (p-value is 0.9996), both models are consistent
HS_twoway=phtest(FE_twoway, RE_twoway)
#Fails to reject the null (p-value is 0.9996)

#POLS VS RE
hs_twoway <- phtest(RE_twoway, POLS) #Fails to reject p value = 0.891, both models are consistent.

### BREUSCH-PAGAN TEST FOR RANDOM EFFECTS
bp_firm <- bptest(RE_firm) #Fails to reject, p value 0.3678, RE is significant
bp_time <- bptest(RE_time) #Fails to reject p value 0.3678, Random effects are significant
bp_twoway <- bptest(RE_twoway) #Fails to reject p value 0.3678, RE is significant
#Also, this shows that there is no significant evidence for heteroskedasticity.


#WOOLDRIDGE TEST FOR CORRELATED ERRORS
residuals_two <- resid(RE_twoway)
individual_effects_two <- resid(RE_twoway, type = "individual")
wooldridge_test <- lmtest::coeftest(lm(residuals_two ~ individual_effects_two))
#The p-value is almost 0, there is perfect collinearity here

bg_test <- bgtest(RE_twoway, order = 1)
#Rejects the null hyptohesis, there is evidence for serial correlation

dw_test <- dwtest(RE_twoway)
#The true autocorrelation is greater than 0.

residuals_firm <- resid(RE_firm)
individual_effects_firm <- resid(RE_firm, type = "individual")
wooldridge_test_firm <- lmtest::coeftest(lm(residuals_firm ~ individual_effects_firm))
#The p-value is almost 0, there is perfect collinearity here

residuals_time <- resid(RE_time)
individual_effects_time <- resid(RE_time, type = "individual")
wooldridge_test_time <- lmtest::coeftest(lm(residuals_time ~ individual_effects_time))
#The p-value is almost 0, there is perfect collinearity here


#So there is no heteroskedasticity but there are correlated errors.


### ROBUST VARIANCE STRATEGIES
library(sandwich)
RE_robust_two <- plm(y~k+l, index=c('ivar', 'tvar'), data=data_prod,  model = "random", effect = "twoways", vcov = vcovHC, method = "arellano")


#Probably we should not include this part, I am not sure if it is informative
bp_test <- bptest(RE_robust_two) #Fails to reject, no heteroskedasticity
robust_resid <- resid(RE_robust_two)
individual_effects_robust <- resid(RE_robust_two, type = "individual")
wooldridge_test_robust <- lmtest::coeftest(lm(robust_resid ~ individual_effects_robust))
#Still rejects the null, p value is 0


#Robust Hausman Test
hausmanTest <- phtest(FE_twoway, RE_twoway, vcov. = vcovHC(FE_twoway, type = "HC1"))
#Fails to reject the null hypothesis. So, both tests are consistent.

#Then we choose the robust random effects estimator.
summary(RE_robust_two)

