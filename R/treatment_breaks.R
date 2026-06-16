library(readxl)
library(survival)
library(survminer)

df <- read_excel("C:/Users/emeri/Documents/Research/Treatment breaks/C-län 151125 Petter.xlsx")

# Kaplan-Meier
km_fit <- survfit(Surv(C_OS_diagnosis, VITALSTATUSUPPDATERAD) ~ 1, data = df)

summary(km_fit)

ggsurvplot(
  km_fit,
  data        = df,
  risk.table  = TRUE,
  conf.int    = TRUE,
  xlab        = "Time",
  ylab        = "Overall survival probability",
  title       = "Kaplan-Meier — Overall Survival"
)
