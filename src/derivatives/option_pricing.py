"""
Author: PMC
Date: 11 Nov 2024

Functions for option pricing
"""

import numpy as np
from scipy.stats import norm

# Black and Scholes

def N(x: float):
    """
    Cumulative Normal Distribution of the Standard Normal Distribution (mean = 0, std = 1)
    """
    return norm.cdf(x)

def N_der(x: float):
    """
    Derivative of N(x). Usefule for Greeks calculation
    """
    return np.exp(-(x**2)/2)/((2*np.pi)**(1/2))

def black_scholes(s0: float, strike: float, annual_vol: float, maturity: float, free_rate: float,
    div_yield: float, call: bool = True) -> float:
    """
    black_scholes
    
    == Summary ==
    Computes the Price of an EU option using the Black-Scholes model
    
    == Args ==
    s0 (float):             Current value of the underlying
    strike (float):         Strike price
    annual_vol (float):     Annual volatility (0 < annual_vol)
    maturity (float):       Number of years until maturity
    free_rate (float):      Annual risk free rate (0 < free_rate)
    div_yield (float):      Annual Dividend yield (0 < div_yield)
    call (bool):            True for Call options, False for Put options
    
    == Returns ==
    (float) Price of the option, using Black-Scholes 
    """
    
    if (annual_vol < 0):
        raise ValueError("black_scholes: Annual Volatility cant be negative")
    
    if (div_yield < 0) :
        raise ValueError("black_scholes: Dividend Yield cant be negative")
    
    if (free_rate < 0):
        raise ValueError("black_scholes: Risk Free Rate cant be negative")
    
    # Adjust the underlying price for the dividend yield
    s0_actual = s0 * np.exp(-div_yield * maturity)
    
    # Compute d1 and d2
    d1 = (np.log(s0/strike) + maturity*(free_rate - div_yield +(annual_vol**2)/2))/(annual_vol*(np.sqrt(maturity))) 
    d2 = d1 - (annual_vol*np.sqrt(maturity))
    
    # Compute Beta + Delta
    beta = -N(d2) if call else (1 - N(d2))
    delta = N(d1) if call else (N(d1) - 1)
    
    return s0_actual*delta + strike*np.exp(-free_rate*maturity)*beta 
    
    
    
def binomial_put(s0: float, strike: float, maturity: int, period_vol: float, period_rate: float,
    period_div: float) -> float:
    """
    binomial_put
    
    == Summary ==
    Computes the Price of an US Put option using the Binomial Model
    
    == Args ==
    s0 (float):             Current value of the underlying
    strike (float):         Strike price
    maturity (int):         Number of periods until maturity
    period_vol (float):     Volatility per period (0 < annual_vol)
    peridod_rate (float):   Risk free rate per period (0 < free_rate)
    period_div (float):     Dividend yield per period (0 < div_yield)
    
    == Returns ==
    (float) Price of the US Put option, using Binomial Model
    """
    # TODO
    return 0


def binomial_call(s0: float, strike: float, maturity: int, period_vol: float, period_rate: float,
    period_div: float) -> float:
    """
    binomial_call
    
    == Summary ==
    Computes the Price of an US Call option using the Binomial Model
    
    == Args ==
    s0 (float):             Current value of the underlying
    strike (float):         Strike price
    maturity (int):         Number of periods until maturity
    period_vol (float):     Volatility per period (0 < annual_vol)
    peridod_rate (float):   Risk free rate per period (0 < free_rate)
    period_div (float):     Dividend yield per period (0 < div_yield)
    
    == Returns ==
    (float) Price of the US Call option, using Binomial Model
    """
    # TODO
    return 0
    
    
def binomial_us(s0: float, strike: float, maturity: float, annual_vol: float, free_rate: float,
    div_yield: float, call: bool = True) -> float:
    """
    binomial_us
    
    == Summary ==
    Returns binomial_call or binomial_put, depending on the option type, defined by arg 'call'
    Calculates the Binomial Model, using monthly periods
    
    == Args ==
    s0 (float):             Current value of the underlying
    strike (float):         Strike price
    maturity (float):       Number of years until maturity
    annual_vol (float):     Annual volatility (0 < annual_vol)
    free_rate (float):      Annual risk free rate (0 < free_rate)
    div_yield (float):      Annual Dividend yield (0 < div_yield)
    
    == Returns ==
    (float) Price of the US option, using Binomial Model
    """
    
    # Months until maturity (rounded because of Python's float "bugs")
    months_to_maturity = round(maturity/(1/12))
    # Monthly volatility
    monthly_vol = annual_vol**(1/12)
    # Monthly risk free rate
    monthly_rate = free_rate**(1/12)
    # Monthly dividend yield
    monthly_div = div_yield**(1/12)
    
    if call:
        return binomial_call(s0, strike, months_to_maturity, monthly_vol, monthly_rate, monthly_div)
    else:
        return binomial_put(s0, strike, months_to_maturity, monthly_vol, monthly_rate, monthly_div)
    
   
   
def option_price(s0: float, strike: float, annual_vol: float, Tyears: float, free_rate: float,
    div_yield: float, vanilla: bool, call: bool = True):
    
    if vanilla:
        return black_scholes(s0, strike, annual_vol, Tyears, free_rate, div_yield, call)
    else:
        s0_actual = s0 * np.exp(-div_yield * Tyears)
        
        # Compute d1
        d1 = (np.log(s0/strike) + Tyears*(free_rate - div_yield +(annual_vol**2)/2))/(annual_vol*(np.sqrt(Tyears))) 
        
        # Compute Delta
        delta = N(d1) if call else (N(d1) - 1)
        
        return s0_actual*delta
        
    
def delta(s0: float, strike: float, annual_vol: float, Tyears: float, free_rate: float,
    div_yield: float, vanilla: bool, call: bool = True):
    
    pheta = 1 if call else -1
    d1 = (np.log(s0/strike) + Tyears*(free_rate - div_yield +(annual_vol**2)/2))/(annual_vol*(np.sqrt(Tyears))) 
            
    
    if vanilla:
        return pheta*np.exp(-div_yield*Tyears)*N(d1*pheta)
    else:
        return pheta*np.exp(-div_yield*Tyears)*N_der(d1)/(annual_vol*np.sqrt(Tyears)) +\
            np.exp(-div_yield*Tyears)*N(pheta*d1)
    
    
def gamma(s0: float, strike: float, annual_vol: float, Tyears: float, free_rate: float,
    div_yield: float, vanilla: bool, call: bool = True):
    
    pheta = 1 if call else -1
    d1 = (np.log(s0/strike) + Tyears*(free_rate - div_yield +(annual_vol**2)/2))/(annual_vol*(np.sqrt(Tyears))) 
    d2 = d1 - (annual_vol*np.sqrt(Tyears))
    
    if vanilla:
        return N_der(d1)*np.exp(-div_yield*Tyears)/(s0*annual_vol*np.sqrt(Tyears))
    else:
        return -pheta*np.exp(-div_yield*Tyears)/(s0*(annual_vol**2)*Tyears)*d2*N_der(d1)
        
    
def vega(s0: float, strike: float, annual_vol: float, Tyears: float, free_rate: float,
    div_yield: float, vanilla: bool, call: bool = True):
    
    pheta = 1 if call else -1
    d1 = (np.log(s0/strike) + Tyears*(free_rate - div_yield +(annual_vol**2)/2))/(annual_vol*(np.sqrt(Tyears))) 
    d2 = d1 - (annual_vol*np.sqrt(Tyears))
    
    if vanilla:
        return s0*np.exp(-div_yield*Tyears)*np.sqrt(Tyears)*N_der(d1)
    else:
        return -(pheta*s0*np.exp(-div_yield*Tyears)/annual_vol)*(d2*N_der(d1))
    
    
def rho(s0: float, strike: float, annual_vol: float, Tyears: float, free_rate: float,
    div_yield: float, vanilla: bool, call: bool = True):
    
    pheta = 1 if call else -1
    d1 = (np.log(s0/strike) + Tyears*(free_rate - div_yield +(annual_vol**2)/2))/(annual_vol*(np.sqrt(Tyears))) 
    d2 = d1 - (annual_vol*np.sqrt(Tyears))
    
    if vanilla:
        return pheta*strike*np.exp(-free_rate*Tyears)*Tyears*N(pheta*(d1-annual_vol*np.sqrt(Tyears)))
    else:
        return pheta*s0*np.exp(-div_yield*Tyears)*np.sqrt(Tyears)*N_der(d1)/annual_vol
        
    