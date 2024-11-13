"""
Author: PMC
Date: 12 Nov 2024

Option Frame definition

== Frame Explanation ==
Option Frame is where the user will input the values for its Option and get outputs
"""

import tkinter as tk

import os
import sys
sys.path.append("../derivatives/options/")

from AppRoot import AppRoot
from option import Option, Period, OptionType, OptionStyle


class OptionFrame(tk.Frame):
    
    id = "Option"
    
    def __init__(self, root: AppRoot, geom: str, option: Option):

        self.bg = "#97c5eb"
        self.fg = "#1f3044"
        super().__init__(root, bg=self.bg)
        self.root = root
        self.option = option
        
    
    def go_back_cb(self):
        """
        Callback for the "Go back" button
        
        It will hide OptionFrame and show PickFrame
        """
        from PickFrame import PickFrame
        
        self.root.show(PickFrame.id)
        self.root.hide(OptionFrame.id)
    
   
    def price_it_cb(self):
        pass
        
        
    def build(self):
        
        # Add "Go Back" button
        go_back_button = tk.Button(
            self,
            text="<- Go Back",
            font=("Arial", 24),
            bg="grey",
            fg="black",
            command=self.go_back_cb
        )   
        
        go_back_button.pack(pady=100)
        go_back_button.place(x=0, y=0, anchor="nw")
        
        # Add "Option" text
        vanilla_option_txt = tk.Label(self, text="Option", font=("Arial", 36, "bold"), fg=self.fg, bg=self.bg)
        vanilla_option_txt.place(x=0,y=100)
        
        ########### INPUTS ###########
        
        input_x_offset = 250
        
        # Price 
        price_tag = tk.Label(self, text="Price (€)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        price_tag.place(x=0, y=200)
        
        price_input = tk.Entry(self,justify="right")
        price_input.insert(0, str(self.option.s0))
        price_input.place(x=input_x_offset, y=200)
        
        
        # Strike Price 
        price_tag = tk.Label(self, text="Strike Price (€)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        price_tag.place(x=0, y=230)
        
        strike_input = tk.Entry(self,justify="right")
        strike_input.insert(0, str(self.option.strike))
        strike_input.place(x=input_x_offset, y=230)
        
        # Period Size
        period_tag = tk.Label(self, text="Period Size", font=("Arial", 14), fg=self.fg, bg=self.bg)
        period_tag.place(x=0, y=260)
        
        period_month = tk.Radiobutton(self, text="Months", var=self.option.period_size,
            value=Period.Months, font=("Arial", 14), fg=self.fg, bg=self.bg)
        period_month.place(x=input_x_offset, y=260)

        period_year = tk.Radiobutton(self, text="Years", var=self.option.period_size, 
            value=Period.Years, font=("Arial", 14), fg=self.fg, bg=self.bg)
        period_year.place(x=input_x_offset+100, y=260)
        
        # Maturity 
        maturity_tag = tk.Label(self, text="Maturity (Periods)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        maturity_tag.place(x=0, y=290)
        
        maturity_input = tk.Entry(self,justify="right")
        maturity_input.insert(0, str(self.option.maturity))
        maturity_input.place(x=input_x_offset, y=290)
        
        # Annual Volatility 
        vol_tag = tk.Label(self, text="Annual Volatility (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        vol_tag.place(x=0, y=320)
        
        vol_input = tk.Entry(self,justify="right")
        vol_input.insert(0, self.option.get_vol_str_perc()[:-2]) # Remove % sign
        vol_input.place(x=input_x_offset, y=320)
        
        # Risk-free Rate 
        frate_tag = tk.Label(self, text="Risk-free rate (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        frate_tag.place(x=0, y=350)
        
        frate_input = tk.Entry(self,justify="right")
        frate_input.insert(0, self.option.get_frate_str_perc()[:-2]) # Remove % sign
        frate_input.place(x=input_x_offset, y=350)
        
        # Dividend Yield 
        div_tag = tk.Label(self, text="Annual Dividend Yield (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        div_tag.place(x=0, y=380)
        
        div_input = tk.Entry(self,justify="right")
        div_input.insert(0, self.option.get_div_yield_str_perc()[:-2]) # Remove % sign
        div_input.place(x=input_x_offset, y=380)
        
        # Option Type
        type_tag = tk.Label(self, text="Option Type", font=("Arial", 14), fg=self.fg, bg=self.bg)
        type_tag.place(x=0, y=410)
        
        type_call = tk.Radiobutton(self, text="Call", var=self.option.option_type,
            value=OptionType.Call, font=("Arial", 14), fg=self.fg, bg=self.bg)
        type_call.place(x=input_x_offset, y=410)

        type_put = tk.Radiobutton(self, text="Put", var=self.option.option_type, 
            value=OptionType.Put, font=("Arial", 14), fg=self.fg, bg=self.bg)
        type_put.place(x=input_x_offset+100, y=410)
        
        # Option Style
        style_tag = tk.Label(self, text="Option Style", font=("Arial", 14), fg=self.fg, bg=self.bg)
        style_tag.place(x=0, y=440)
        
        style_us = tk.Radiobutton(self, text="US", var=self.option.option_style,
            value=OptionStyle.US, font=("Arial", 14), fg=self.fg, bg=self.bg)
        style_us.place(x=input_x_offset, y=440)

        style_eu = tk.Radiobutton(self, text="EU", var=self.option.option_style, 
            value=OptionStyle.EU, font=("Arial", 14), fg=self.fg, bg=self.bg)
        style_eu.place(x=input_x_offset+100, y=440)
        
        ###### END OF INPUTS #######
        
        
        # Price It Button
        
