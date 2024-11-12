"""
Author: PMC
Date: 12 Nov 2024

Definition of Option class
"""

from option_pricing import *
from enum import Enum

class Period(Enum):
    Years = 1
    Months = 2
    
class OptionType(Enum):
    Call = 1
    Put = 2
    
class OptionStyle(Enum):
    EU = 1
    US = 2 
    

class Option:
    """
    Option
    
    == Summary ==
    Class that represents a Vanilla Option
    
    == Attributes ==
    s0 (float):                 Current value of the underlying
    strike (float):             Strike Price value     
    maturity (int)              Periods to Maturity
    period_size (Period)        Duration of Periods (Monthly or Yearly)
    annual_vol (float)          Annual Volatility (0 < annual_vol < 1)
    free_rate (float)           Annual risk-free rate (0 < free_rate < 1)
    div_yield (float)           Annual dividend yield (0 < div_yield < 1)
    option_type (OptionType)    Option Type (Call/Put)
    option_style OptionStyle)   Option Style (US/EU)
    """
    
    
    def __init__(self):
        
        # Every new instance of an option will be init with values for all its attributes

        self.s0:            float       = 100
        self.strike:        float       = 100
        self.period_size:   Period      = Period.Years
        self.maturity:      int         = 3
        self.annual_vol:    float       = 0.1
        self.free_rate:     float       = 0.03
        self.div_yield:     float       = 0.01
        self.option_type:   OptionType  = OptionType.Call
        self.option_style:  OptionStyle = OptionStyle.EU
        
    # Protected Setters
    
    def set_s0(self, s0_str: str): 
        try:
            s0_nr = float(s0_str)
        except:
            raise ValueError("Option: Underlying value must be a number")

        self.s0 = round(s0_nr, 2)
        
    def set_strike(self, strike_str: str): 
        try:
            strike_nr = float(strike_str)
        except:
            raise ValueError("Option: Strike value must be a number")

        self.strike = round(strike_nr, 2)
        
    def set_maturity(self, maturity_str: str):
        try:
            maturity_nr = float(maturity_str)
        except:
            raise ValueError("Option: Maturity must be a number")

        self.maturity = round(maturity_nr, 2)
        
    def set_volatility(self, vol_str: str):
        try:
            vol_nr = float(vol_str)
        except:
            raise ValueError("Option: Volatility must be a number")
        
        if (vol_nr > 1) or (vol_nr < 0):
            raise ValueError("Option: Volatility must be between 0 and 1")

        self.annual_vol = round(vol_nr, 2)
        
    def set_free_rate(self, rate_str: str):
        try:
            rate_nr = float(rate_str)
        except:
            raise ValueError("Option: Risk-Free Rate must be a number")
        
        if (rate_nr > 1) or (rate_nr < 0):
            raise ValueError("Option: Risk-Free Rate must be between 0 and 1")

        self.free_rate = round(rate_nr, 2)
        
    def set_div_yiled(self, div_str: str):
        try:
            div_nr = float(div_str)
        except:
            raise ValueError("Option: Dividend Yield must be a number")
        
        if (div_nr > 1) or (div_nr < 0):
            raise ValueError("Option: Dividend Yield must be between 0 and 1")

        self.div_yield = round(div_nr, 2)
        
        
    def price(self) -> float:
        """
        price
        
        == Summary ==
        Returns the price of the option (int), using Black-Scholes if it is an EU option, 
        Binomial Model, otherwise
        """
        
        # Amount of years until maturity (ex.: 1.5 -> 1 year and a half)
        maturity_years = self.maturity if (self.period_size is Period.Years) else self.maturity/12 
        # Whether the option is a Call (True) or a Put (False) 
        is_call = (self.option_type is OptionType.Call)
        
        if (self.option_style is OptionStyle.EU):
            
            # If EU option, will use Black Scholes
            return black_scholes(self.s0, self.strike, self.annual_vol, maturity_years, self.free_rate, 
                self.div_yield, call=is_call)
            
        else:
            
            # If US option, will use Binomial Model
            return binomial_us(self.s0, self.strike, maturity_years, self.annual_vol, self.free_rate,
                self.div_yield, call=is_call)
            
            
    def write_report(self):
        pass