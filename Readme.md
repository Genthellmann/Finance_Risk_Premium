# Economic Uncertainty in the Starting Phase of the Corona Crisis

This repository contains the code for the seminar paper. 

## Introduction

As the corona pandemic progresses in early 2020, VSTOXX premiums continue to fall. Puzzlingly, the more uncertainty increases, the more premiums fall. When the WHO declares the coronavirus a pandemic on March 11, the VSTOXX jumps to 72 on the closest day and the VSTOXX premium falls to -13. Obviously, futures prices react inadequately when uncertainty increases and the market underestimates risk. The underestimation of risk when volatility increases is even increasing. The question now is whether this behavior occurs randomly and uniquely during the corona pandemic due to the short time period or whether a pattern emerges. If a pattern is evident, it is a systemically inadequate response. Thus, a trading strategy that uses VSTOXX premiums as a buy indicator can generate large risk-adjusted returns: "the low premium response puzzle".



**Prepare_Dataset_correctEOM.py** prepares the data for the ARMA-Model: The one-month premium combines premiums of different futures into a time series and refers to the future expiring in the next month. On the last day of each month, the premium is "rolled forward".

**VIXP_Arma.py** estimates the ARMA Model to forecast the premium.

**TStrategies.py** includes the different Trading Strategies to exploit the indications given by the premium with L=Long, S=Short, C=Cash.


## Remark
A lot of the written code follows the style of an interactive Approach. A more automated version is currently developed and will be published first on the development branch. 