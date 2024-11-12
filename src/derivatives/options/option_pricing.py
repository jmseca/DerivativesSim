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

def black_scholes(s0: float, strike: float, annual_vol: float, maturity: float, free_rate: float,
    div_yield: float, call: bool = True) -> float:
    """
    black_scholes
    
    == Summary ==
    Computes the Price of an EU option using the Black-Scholes model
    
    == Args ==
    s0 (float):             Current value of the underlying
    strike (float):         Strike price
    annual_vol (float):     Annual volatility (0 < annual_vol < 1)
    maturity (float):       Number of years until maturity
    free_rate (float):      Annual risk free rate (0 < free_rate < 1)
    div_yield (float):      Annual Dividend yield (0 < div_yield < 1)
    call (bool):            True for Call options, False for Put options
    
    == Returns ==
    (float) Price of the option, using Black-Scholes 
    """
    
    if (annual_vol < 0) or (annual_vol > 1):
        raise ValueError("black_scholes: Annual Volatility must be between 0 and 1")
    
    if (div_yield < 0) or (div_yield > 1):
        raise ValueError("black_scholes: Dividend Yield must be between 0 and 1")
    
    if (free_rate < 0) or (free_rate > 1):
        raise ValueError("black_scholes: Risk Free Rate must be between 0 and 1")
    
    # Take the underlying's dividend into account
    s0_actual = s0*((1-div_yield)**maturity)
    
    # Compute d1 and d2
    d1 = np.log(s0_actual/(strike*np.exp(-maturity*free_rate)))/(annual_vol*(maturity**(1/2))) + \
        (annual_vol*(maturity**(1/2)))/2
    d2 = d1 - (annual_vol*(maturity**(1/2)))
    
    # Compute Beta + Delta
    beta = -N(d2) if call else (1 - N(d2))
    delta = N(d1) if call else (N(d1) - 1)
    
    return s0*delta + strike*beta #TODO: Check if this with s0 or s0_actual
    
    
    
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
    period_vol (float):     Volatility per period (0 < annual_vol < 1)
    peridod_rate (float):   Risk free rate per period (0 < free_rate < 1)
    period_div (float):     Dividend yield per period (0 < div_yield < 1)
    
    == Returns ==
    (float) Price of the US Put option, using Binomial Model
    """
    pass


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
    period_vol (float):     Volatility per period (0 < annual_vol < 1)
    peridod_rate (float):   Risk free rate per period (0 < free_rate < 1)
    period_div (float):     Dividend yield per period (0 < div_yield < 1)
    
    == Returns ==
    (float) Price of the US Call option, using Binomial Model
    """
    pass
    
    
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
    annual_vol (float):     Annual volatility (0 < annual_vol < 1)
    free_rate (float):      Annual risk free rate (0 < free_rate < 1)
    div_yield (float):      Annual Dividend yield (0 < div_yield < 1)
    
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