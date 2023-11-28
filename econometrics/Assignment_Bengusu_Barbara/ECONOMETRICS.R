## Econometrics Assignment R Code
## Group Number:
## Group Members: Barbara Karwowska & Bengusu Nar

# Data used

interest_rate <-read.csv("shortinterest.csv")
interest_rate_m <-read.csv("interest_rates_short_term_monthly.csv")
inflation <-read.csv("inflation_y.csv")
inflation_m <-read.csv("inflation_m.csv")
output_gap <-read.csv("output_gap.csv")
exchange_usa <-read.csv("yearly_exchange.csv")
exchange_china <- read.csv("china_exchange.csv") # CNY
exchange_uk <- read.csv("uk_exchange.csv") #In dollars
inflation_lag1 <- read.csv("inflation_lag.csv")
inflation_lag2 <- read.csv("inflation_lag_2.csv")

## MODEL BASED ON TAYLOR'S FORMULA USING MONTHLY DATA

# Unfortunately we do not have monthly data on the output gap and the output.
# Hence, to increase the number of observations, we need to interpolate 
# assuming a constant rate of change of the output gap thoughout given years.

# Function we used for interpolation.

interpolation <- function(df) {
  df$val_interp[df$month == 1] <- df$Value[df$month == 1]
  (acs <- rep(NA, 12))
  df$interp_lag <- c(df$val_interp[13:(length(df$val_interp))],acs);
  df$diff <- c(df$val_interp - df$interp_lag)
  
  for (i in min:(max-1)) {
    for (j in 2:13) {
      init = df$val_interp[df$month==1 & df$year == i]
      end=df$interp_lag[df$month==1 & df$year == i]
      record=which(df$month==j & df$year==i)
      record1=which(df$month==1 & df$year==i)
      if (init  < end) {
        df$val_interp[record]<- df$val_interp[record1] +
          abs(df$diff[record1])/12*(j-1)
      }  
      else {
        df$val_interp[record] <-
          df$val_interp[record1] -
          abs(df$diff[record1])/12*(j-1)
      }
    }
  }
  
  return(df)
}

(N <- sum(!is.na(output_gap$Value)))
(min <- min(output_gap$Time))
(max <- max(output_gap$Time))
month <- rep(1:12, each=1, times=N)
year <- rep(min:max, each=12, times=1)
(month_df <- data.frame(month, year))
output_gap_m <- merge(x = month_df, y = output_gap, by.x = "year",
                      by.y = "Time", all = TRUE)
output_gap_m <- output_gap_m[1:(N*12-11),]
output_gap_m <- interpolation(output_gap_m)
gap_m <- output_gap_m$val_interp

# For Taylor's formula we need inflation target which is 2% for France
pi_m_t <-rep(2, times=181)
delta_pi_m <- (inflation_m$Value)[1:181] - pi_m_t
i_m <- (interest_rate_m$Value)[1:181]

data1 <- data.frame(i_m, delta_pi_m, gap_m)
reg_m <- lm(i_m ~ delta_pi_m + gap_m)
summary(reg_m) # high significance levels obtained for all variables and intercept
# however, multiple R-squared of 0.5936 does not indicate strong linear relation

# OLS tests

resettest(reg_m) # as hinted by R^2, very low p-value so evidence against linearity
errors1 = predict(reg_m, data1) - i_m
jarque.bera.test(errors1) # very low p-value so evidence against normality of errors
bgtest(reg_m) # very low p-value so evidence against uncorrelation of errors
bptest(reg_m) # since errors are not normal as shown, we cannot use the
# standard Breusch-Pagan test, but weak OLS assumptions are satisfied so we
# use studentized Breusch-Pagan test (White test) 
# we get a low p value, so there is evidence against homocesdacity

# We have non-linearity as well as correlated and heteroscedastic errors, 
# probably due to interpolation.

# We will therefore examine the annual data

pi_y_t <- rep(2, times = 16)
delta_pi_y <- inflation$Value - pi_y_t
output_gap_y <- output_gap$Value
i_y <- interest_rate$Value

data2 <- data.frame(i_y, delta_pi_y, output_gap_y)
reg_y <- lm(i_y ~ delta_pi_y + output_gap_y)
summary(reg_y) # delta_pi_y is not significant, output_gap_y is
# coefficient of determination is slightly improved

# OLS tests

resettest(reg_y) # low value for linearity
errors2 = predict(reg_y, data2) - i_y
jarque.bera.test(errors2) # high p-value, evidence for normally distributed errors
bgtest(reg_y) # low p-value so evidence against uncorrelated errors
bptest(reg_y) # high p-value so evidence for homocesdacity


# We have evidence for homocesdacity, but still evidence against linearity 
# and uncorrelated errors, so we suspect omitted variables: exchange rates
# and historical inflation rates.


### Exchange rates
# Data on exchange rates against USD are available on OECD website so we obtain
# The EURCNY and EURGPB interest rates indirectly.

usd = exchange_usa$Value #USDEUR
cny = usd / exchange_china$Value #CNYEUR
gbp = usd / exchange_uk$Value #GBPEUR

reg_exchanges <- lm(i_y ~ delta_pi_y + output_gap_y + usd + cny + gbp)
summary(reg_exchanges) # insignificant results as we added too many possibly
# correlated variables, we should deduct the most insignificant: delta_piy

reg_exchanges2 <- lm(i_y ~ output_gap_y + usd + cny + gbp)
summary(reg_exchanges2) # still some insignificant results in exchange rates
# due to possible correlation so we retain the most significant (also the
# exchange rate of the biggest trading partner - US), usd

reg_exchange <- lm(i_y ~ delta_pi_y + output_gap_y + usd)
summary(reg_exchange) # delta_piy is still insignificant, while usd has now
# approximately significance level of 0.01, so we discard delta_piy

reg_exchange2 <- lm(i_y ~ output_gap_y + usd)
summary(reg_exchange2) # high significance, so we run OLS tests

# OLS TESTS

data3 <- data.frame(i_y, output_gap_y, usd)
errors3 = predict(reg_exchange2, data3) - i_y
jarque.bera.test(errors3) # very low p value - evidence against normality of errors 
resettest(reg_exchange2) # high p-value so evidence for the linearity
bgtest(reg_exchange2) # high p-value so evidence for uncorrelated errors
bptest(reg_exchange2) # since errors are not normal as shown, we cannot use the
# standard Breusch-Pagan test, but weak OLS assumptions are satisfied so we
# use studentized Breusch-Pagan test (White test) 
# we get a high p value, so there is evidence for homocesdacity




### Inflation with lag 

# We suspect that monetary policy adjusts with a delay in response to the inflation
# so instead of considering the current inflation rates, we consider past inflation
# rates: from last year (data from 2002 to 2017) and from two years ago
# (data from 2001 to 2016)

inflation_y_lag1 <- inflation_lag1$Value # regression of current interest rate
# on the past year's inflation rate and the output gap
delta_piy_lag1 <- inflation_y_lag1 - pi_y_t
reg_lag1 <- lm(i_y ~ delta_piy_lag1 + output_gap_y)
summary(reg_lag1) # improved significance level compared to current inflation rate
# but still not significant enough (0.134)


inflation_y_lag2 <- inflation_lag2$Value # regression of current interest rate
# on the inflation rate from 2 years ago and the output gap
delta_piy_lag2 <- inflation_y_lag2 -pi_y_t
reg_lag2 <- lm(i_y ~ delta_piy_lag2 + output_gap_y)
summary(reg_lag2) # improved significance level - 0.0758, but still slightly fails
# with respect to 5% significance level

## Let's plot our guess and the real rate
i_predict = predict(reg_exchange2, data3)
year = seq(2003, 2018)
plot(year , i_y, col = "red", ylab="annual interest rate")
lines(year, i_predict)
