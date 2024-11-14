"""
Author: PMC
Date: 12 Nov 2024

Definition of Option class
"""

from option_pricing import *
from enum import Enum

import pandas as pd
import numpy as np

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
        
        
    def is_call(self):
        
        return self.option_type is OptionType.Call
            
    # Protected Setters
    
    def set_s0(self, s0_str: str): 
        try:
            s0_nr = float(s0_str)
        except:
            raise ValueError("Option: Current Asset Price must be a number")

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
        
        if (vol_nr < 0):
            raise ValueError("Option: Volatility cant be negative")

        self.annual_vol = round(vol_nr/100, 5)
        
    def set_free_rate(self, rate_str: str):
        try:
            rate_nr = float(rate_str)
        except:
            raise ValueError("Option: Risk-Free Rate must be a number")
        
        if (rate_nr < 0):
            raise ValueError("Option: Risk-Free Rate  cant be negative")

        self.free_rate = round(rate_nr/100, 5)
        
    def set_div_yiled(self, div_str: str):
        try:
            div_nr = float(div_str)
        except:
            raise ValueError("Option: Dividend Yield must be a number")
        
        if (div_nr < 0):
            raise ValueError("Option: Dividend Yield cant be negative")

        self.div_yield = round(div_nr/100, 5)
        
    # Getters
    
    def get_years_to_maturity(self) -> float:
        
        return self.maturity if (self.period_size is Period.Years) else round(self.maturity*(1/12),2)
    
    
    def get_option_type(self) -> str:
        
        return "Call" if (self.option_type is OptionType.Call) else "Put"
    
    def get_vol_str_perc(self) -> str:
        return str(round(self.annual_vol*100,2))+' %'
        
    def get_frate_str_perc(self) -> str:
        return str(round(self.free_rate*100,2))+' %'
        
    def get_div_yield_str_perc(self) -> str:
        return str(round(self.div_yield*100,2))+' %'
        
        
        
    def price(self) -> float:
        raise NotImplementedError("Not Implemented Error")
            
    def delta(self) -> float:
        raise NotImplementedError("Not Implemented Error")
         
    def gamma(self) -> float:
        raise NotImplementedError("Not Implemented Error")
    
    def vega(self) -> float:
        raise NotImplementedError("Not Implemented Error")
    
    def rho(self) -> float:
        raise NotImplementedError("Not Implemented Error")
        
            
            
    def to_text(self):
        opt_type = "Call" if (self.option_type is OptionType.Call) else "Put"
        return f"\
            • Current Asset Price   {self.s0} €\n\
            • Strike Price          {self.strike} €\n\
            • Years to Maturity     {self.get_years_to_maturity()}\n\
            • Annual Volatility     {round(self.annual_vol*100,2)}\n\
            • Risk-free rate        {round(self.free_rate*100,2)}\n\
            • Dividend Yield        {round(self.div_yield*100,2)}\n\
            • Type                  {opt_type}\n\
        "
            
            
    def copy(self) :
        raise NotImplementedError("Not Implemented Error")
        
        
class VanillaOption(Option):
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

        super().__init__()
        self.option_style:  OptionStyle = OptionStyle.EU
        
    def get_option_style(self) -> str:
        
        return "US" if (self.option_style is OptionStyle.US) else "EU"
            
        
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
            
    def delta(self) -> float:
        """
        Get Vanilla Option Delta
        """
        
        # Amount of years until maturity (ex.: 1.5 -> 1 year and a half)
    
        
        if (self.option_style is OptionStyle.EU):
            # EU
            Tyears = self.get_years_to_maturity()
            pheta = 1 if (self.option_type is OptionType.Call) else -1
            d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
            
            return pheta*np.exp(-self.div_yield*Tyears)*N(d1*pheta)
            
        else:
            # US
            raise NotImplementedError("Not Implemented Error")
         
            
    def gamma(self) -> float:
        """
        Get Vanilla Option Gamma
        """
        
        if (self.option_style is OptionStyle.EU):
            # EU
            Tyears = self.get_years_to_maturity()
            d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
            
            return N_der(d1)*np.exp(-self.div_yield*Tyears)/(self.s0*self.annual_vol*np.sqrt(Tyears))
        else:
            # US
            raise NotImplementedError("Not Implemented Error")
        
    def vega(self) -> float:
        if (self.option_style is OptionStyle.EU):
            # EU
            Tyears = self.get_years_to_maturity()
            d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
            
            return self.s0*np.exp(-self.div_yield*Tyears)*np.sqrt(Tyears)*N_der(d1)
        else:
            # US
            raise NotImplementedError("Not Implemented Error")
        
        
    def rho(self) -> float:
        if (self.option_style is OptionStyle.EU):
            # EU
            Tyears = self.get_years_to_maturity()
            pheta = 1 if (self.option_type is OptionType.Call) else -1
            d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
            
            return pheta*self.strike*np.exp(-self.free_rate*Tyears)*Tyears*N(pheta*(d1-self.annual_vol*np.sqrt(Tyears)))
        else:
            # US
            raise NotImplementedError("Not Implemented Error")
            
            
    def to_text(self):
        style = "EU" if (self.option_style is OptionStyle.EU) else "US"
        
        option_txt = super().to_text()
        return f"{option_txt}\
            • Style                 {style}\n"
            
            
    def copy(self) :
        
        new_op = VanillaOption()
        
        new_op.s0           = self.s0
        new_op.strike       = self.strike
        new_op.maturity     = self.maturity
        new_op.annual_vol   = self.annual_vol
        new_op.period_size  = self.period_size
        new_op.free_rate    = self.free_rate
        new_op.div_yield    = self.div_yield
        new_op.option_style = self.option_style
        new_op.option_type  = self.option_type
        
        return new_op
    
    
class AssetOrNothinOption(Option):
    """
    - St if St >  X
    - 0  if St <= X
    
    """
    
    def __init__(self):
        
        # Every new instance of an option will be init with values for all its attributes

        super().__init__()
        self.nr_sims = 10_000
        # 1 period per 2d
        self.delta_t = 1/183    
        
        Tyears = self.get_years_to_maturity()
        self.sims_df = pd.DataFrame(np.random.standard_normal(size=(int(Tyears/self.delta_t + 1), self.nr_sims)))
        
        # Paths used for pricing 
        self.normal_path = self.generate_sample_path(self.s0)
        # Paths used to compute the greeks
        self.greek_path = self.generate_sample_path(self.s0*1.001)
        
    def generate_sample_path(self, price):
        
        "Df with all the simulated asse prices at maturity"
    
        sims_df_factor = (
            (self.sims_df * self.annual_vol * np.sqrt(self.delta_t)) + (self.free_rate * self.delta_t) + 1)
        sims_df_factor.iloc[0] = price
        return sims_df_factor.cumprod()
    
    
    def price(self):
        """
        Price of the AssetOrNothing Option
        """
        
        Tyears = self.get_years_to_maturity()
        call = self.option_type is OptionType.Call
        
        # Adjust the underlying price for the dividend yield
        s0_actual = self.s0 * np.exp(-self.div_yield * Tyears)
        
        # Compute d1
        d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
        
        pheta = 1 if call else -1
        
        return s0_actual*N(pheta*d1)
        
        
    def delta(self):
        """
        Delta
        """
        Tyears = self.get_years_to_maturity()
        pheta = 1 if (self.option_type is OptionType.Call) else -1
        d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
        
        return pheta*np.exp(-self.div_yield*Tyears)*N_der(d1)/(self.annual_vol*np.sqrt(Tyears)) +\
            np.exp(-self.div_yield*Tyears)*N(pheta*d1)
        
        
        
    def gamma(self):
        """
        Gamma
        """
        Tyears = self.get_years_to_maturity()
        pheta = 1 if (self.option_type is OptionType.Call) else -1
        d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
        d2 = d1 - (self.annual_vol*np.sqrt(Tyears))
        
        return -pheta*np.exp(-self.div_yield*Tyears)/(self.s0*(self.annual_vol**2)*Tyears)*d2*N_der(d1)
    
    
    def vega(self):
        """
        Vega
        """
        Tyears = self.get_years_to_maturity()
        pheta = 1 if (self.option_type is OptionType.Call) else -1
        d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
        d2 = d1 - (self.annual_vol*np.sqrt(Tyears))
        
        return -(pheta*self.s0*np.exp(-self.div_yield*Tyears)/self.annual_vol)*(d2*N_der(d1))
    
    
    def rho(self):
        """
        Rho
        """
        Tyears = self.get_years_to_maturity()
        pheta = 1 if (self.option_type is OptionType.Call) else -1
        d1 = (np.log(self.s0/self.strike) + Tyears*(self.free_rate - self.div_yield +(self.annual_vol**2)/2))/(self.annual_vol*(np.sqrt(Tyears))) 
        
        return pheta*self.s0*np.exp(-self.div_yield*Tyears)*np.sqrt(Tyears)*N_der(d1)/self.annual_vol
        
        

