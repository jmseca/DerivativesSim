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
sys.path.append("../derivatives/")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from AppRoot import AppRoot
from options import Option, Period, OptionType, OptionStyle
from option_pricing import black_scholes#, delta, gamma

from enum import Enum

class VisualType(Enum):
    
    Vol = 1,
    Mat = 2
    Rf = 3,
    


class VisualFrame(tk.Frame):
    
    vol_id = "volatility"
    mat_id = "maturity"
    rf_id = "riskfree"  
    
    # Canvas + Lines IDs
    price = "price"
    delta = "delta"  
    
    def __init__(self, root: AppRoot, geom: str, vtype: VisualType):

        self.bg = "#97c5eb"
        
        super().__init__(root, bg=self.bg)
        self.fg = "#1f3044"
        self.root = root
        self.visual_type = vtype
        self.built = -1
        self.slider_labels = "Volatility" if vtype is VisualType.Vol else "Maturity (yrs)" if vtype is VisualType.Mat else "Risk-free rate"
        
        
        
        
        self.canvas = {}
        self.lines = {}
        
    
    def go_back_cb(self):
        """
        Callback for the "Go back" button
        
        It will hide OptionFrame and show PickFrame
        """
        from OptionFrame import OptionFrame
        
        if self.vanilla:
            self.root.show(OptionFrame.vanilla_id)
        else:
            self.root.show(OptionFrame.exotic_id)
            
            
        if self.visual_type is VisualType.Mat:
            self.root.hide(VisualFrame.mat_id)
        elif self.visual_type is VisualType.Vol:
            self.root.hide(VisualFrame.vol_id)
        else:
            self.root.hide(VisualFrame.rf_id)
            
        
        
    def go_right_cb(self):
        
        
        if self.visual_type is VisualType.Mat:
            self.root.show(VisualFrame.rf_id)
            self.root.hide(VisualFrame.mat_id)
        elif self.visual_type is VisualType.Vol:
            self.root.show(VisualFrame.mat_id)
            self.root.hide(VisualFrame.vol_id)

        
    def go_left_cb(self):
    
        if self.visual_type is VisualType.Mat:
            self.root.show(VisualFrame.vol_id)
            self.root.hide(VisualFrame.mat_id)
        elif self.visual_type is VisualType.Rf:
            self.root.show(VisualFrame.mat_id)
            self.root.hide(VisualFrame.rf_id)
            
            
    def update_price(self, val):
        
        val = float(val)
        
        if self.visual_type is VisualType.Mat:
            
            y_values = black_scholes(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                val, 
                self.option.free_rate,
                self.option.div_yield,
                self.option.is_call()
            )
            
        elif self.visual_type is VisualType.Vol:
            
            y_values = black_scholes(
                self.x_values,
                self.option.strike,
                val,
                self.option.get_years_to_maturity(), 
                self.option.free_rate,
                self.option.div_yield,
                self.option.is_call()
            )
            
        else:
            
            y_values = black_scholes(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                self.option.get_years_to_maturity(), 
                val,
                self.option.div_yield,
                self.option.is_call()
            )
            
        print(y_values)
        self.lines[VisualFrame.price].set_ydata(y_values)
        self.canvas[VisualFrame.price].draw()
        
        
    def build(self, vanilla: bool, option: Option):
        
        if self.built == 0:
            return
        self.built = 0
        self.vanilla = vanilla
        self.option = option
        # Asset Price Values
        self.x_values = np.linspace(0.01,option.s0*2,50)
        
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
        
        # TODO: missing title
        # Add "Option" text
        #vanilla_option_txt = tk.Label(self, text="Option", font=("Arial", 36, "bold"), fg=self.fg, bg=self.bg)
        #vanilla_option_txt.place(x=0,y=100)
        
        ########### GRAPHS ###########
        
        # Option Price
        
        price_fig, price_ax = plt.subplots(figsize=(5, 3))
        price_y = black_scholes(
            self.x_values,
            self.option.strike,
            self.option.annual_vol,
            self.option.get_years_to_maturity(), 
            self.option.free_rate,
            self.option.div_yield,
            self.option.is_call()
        )
        price_line, = price_ax.plot(self.x_values, price_y, lw=2)
        self.lines[VisualFrame.price] = price_line
        
        price_canvas = FigureCanvasTkAgg(price_fig, master=self)
        price_canvas.get_tk_widget().place(x=10,y=100, width=500)
        self.canvas[VisualFrame.price] = price_canvas
        
        price_vol_slider = tk.Scale(self, from_=0, to=1, orient="horizontal", label=self.slider_labels, resolution=0.01, command=self.update_price)
        price_vol_slider.set(self.option.annual_vol)
        price_vol_slider.place(x=10, y=400)
        price_vol_slider.config(length=500)
        
        """
        # Strike Price 
        strike_tag = tk.Label(self, text="Strike Price (€)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        strike_tag.place(x=0, y=230)
        
        strike_input = tk.Entry(self,justify="right")
        strike_input.insert(0, str(self.option.strike))
        strike_input.place(x=input_x_offset, y=230)
        # Add it to inputs
        self.inputs[OptionFrame.strike] = strike_input
        
        # Period Size
        period_tag = tk.Label(self, text="Period Size", font=("Arial", 14), fg=self.fg, bg=self.bg)
        period_tag.place(x=0, y=260)
        
        period_control_var = tk.IntVar(value=(1 if self.option.period_size is Period.Months else 2))
        self.inputs[OptionFrame.period_size] = period_control_var
        
        period_month = tk.Radiobutton(self, text="Months", var=period_control_var,
            value=1, font=("Arial", 14), fg=self.fg, bg=self.bg, command=self.set_period_cb)
        period_month.place(x=input_x_offset, y=260)

        period_year = tk.Radiobutton(self, text="Years", var=period_control_var, 
            value=2, font=("Arial", 14), fg=self.fg, bg=self.bg, command=self.set_period_cb)
        period_year.place(x=input_x_offset+100, y=260)
        
        # Maturity 
        maturity_tag = tk.Label(self, text="Maturity (Periods)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        maturity_tag.place(x=0, y=290)
        
        maturity_input = tk.Entry(self,justify="right")
        maturity_input.insert(0, str(self.option.maturity))
        maturity_input.place(x=input_x_offset, y=290)
        # Add it to inputs
        self.inputs[OptionFrame.maturity] = maturity_input
        
        # Annual Volatility 
        vol_tag = tk.Label(self, text="Annual Volatility (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        vol_tag.place(x=0, y=320)
        
        vol_input = tk.Entry(self,justify="right")
        vol_input.insert(0, self.option.get_vol_str_perc()[:-2]) # Remove % sign
        vol_input.place(x=input_x_offset, y=320)
        # Add it to inputs
        self.inputs[OptionFrame.vol] = vol_input
        
        # Risk-free Rate 
        frate_tag = tk.Label(self, text="Risk-free rate (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        frate_tag.place(x=0, y=350)
        
        frate_input = tk.Entry(self,justify="right")
        frate_input.insert(0, self.option.get_frate_str_perc()[:-2]) # Remove % sign
        frate_input.place(x=input_x_offset, y=350)
        # Add it to inputs
        self.inputs[OptionFrame.frate] = frate_input
        
        
        # Dividend Yield 
        div_tag = tk.Label(self, text="Annual Dividend Yield (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        div_tag.place(x=0, y=380)
        
        div_input = tk.Entry(self,justify="right")
        div_input.insert(0, self.option.get_div_yield_str_perc()[:-2]) # Remove % sign
        div_input.place(x=input_x_offset, y=380)
        # Add it to inputs
        self.inputs[OptionFrame.div] = div_input
        
        # Option Type
        type_tag = tk.Label(self, text="Option Type", font=("Arial", 14), fg=self.fg, bg=self.bg)
        type_tag.place(x=0, y=410)
        
        type_control_var = tk.IntVar(value=(1 if self.option.option_type is OptionType.Call else 2))
        self.inputs[OptionFrame.option_type] = type_control_var
        
        type_call = tk.Radiobutton(self, text="Call", var=type_control_var,
            value=1, font=("Arial", 14), fg=self.fg, bg=self.bg, command=self.set_type_cb)
        type_call.place(x=input_x_offset, y=410)

        type_put = tk.Radiobutton(self, text="Put", var=type_control_var, 
            value=2, font=("Arial", 14), fg=self.fg, bg=self.bg, command=self.set_type_cb)
        type_put.place(x=input_x_offset+100, y=410)
        
        # Option Style
        #style_tag = tk.Label(self, text="Option Style", font=("Arial", 14), fg=self.fg, bg=self.bg)
        #style_tag.place(x=0, y=440)
        
        # Var that controls the binary choice
        #style_control_var = tk.IntVar(value=(1 if self.option.option_style is OptionStyle.US else 2))
        #self.inputs[OptionFrame.style] = style_control_var
        
        #style_us = tk.Radiobutton(self, text="US", var=style_control_var,
        #    value=1, font=("Arial", 14), fg=self.fg, bg=self.bg, command=self.set_style_cb)
        #style_us.place(x=input_x_offset, y=440)

        #style_eu = tk.Radiobutton(self, text="EU", var=style_control_var, 
        #    value=2, font=("Arial", 14), fg=self.fg, bg=self.bg, command=self.set_style_cb)
        #style_eu.place(x=input_x_offset+100, y=440)
        
        
        
        ###### END OF INPUTS #######
        
        # Error Label
        
        error_tag = tk.Label(self, text="Option Style", font=("Arial", 14, "bold"), fg="red", bg=self.bg)
        self.inputs[OptionFrame.error] = error_tag
        
        # Price It Button
        
        price_button = tk.Button(
            self,
            text="Price it",
            font=("Arial", 24, "bold"),
            bg="#1f3044",
            fg="#f0f3f5",
            width=20,
            height=2,
            command=self.price_it_cb 
        )   
        price_button.pack(pady=100)
        price_button.place(x=100, y=600)
        
        
        ######## OUTPUTS #########
        
        # Add Price 
        price_tag = tk.Label(self, text="Price", font=("Arial", 26, "bold"), fg=self.fg, bg=self.bg)
        price_tag.place(x=1000, y=150)
        
        price_label = tk.Label(self, text=f"{round(self.option.price(),2)} €", font=("Arial", 26, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        price_label.place(x=1000, y=200, width=300, height=50)
        self.outputs[OptionFrame.price_label] = price_label
        
        
        ### GREEKS ###
        
        # Delta
        delta_tag = tk.Label(self, text="Delta", font=("Arial", 18, "bold"), fg=self.fg, bg=self.bg)
        delta_tag.place(x=1000, y=280)
        
        delta_label = tk.Label(self, text=f"{round(self.option.delta(),2)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        delta_label.place(x=1000, y=310, width=300, height=35)
        self.outputs[OptionFrame.delta_label] = delta_label
        
        # Gamma
        gamma_tag = tk.Label(self, text="Gamma", font=("Arial", 18, "bold"), fg=self.fg, bg=self.bg)
        gamma_tag.place(x=1000, y=350)
        
        gamma_label = tk.Label(self, text=f"{round(self.option.gamma(),2)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        gamma_label.place(x=1000, y=380, width=300, height=35)
        self.outputs[OptionFrame.gamma_label] = gamma_label
        
        # Vega
        vega_tag = tk.Label(self, text="Vega", font=("Arial", 18, "bold"), fg=self.fg, bg=self.bg)
        vega_tag.place(x=1000, y=420)
        
        vega_label = tk.Label(self, text=f"{round(self.option.vega(),2)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        vega_label.place(x=1000, y=450, width=300, height=35)
        self.outputs[OptionFrame.vega_label] = vega_label
        
        # Rho
        rho_tag = tk.Label(self, text="Rho", font=("Arial", 18, "bold"), fg=self.fg, bg=self.bg)
        rho_tag.place(x=1000, y=490)
        
        rho_label = tk.Label(self, text=f"{round(self.option.rho(),2)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        rho_label.place(x=1000, y=520, width=300, height=35)
        self.outputs[OptionFrame.rho_label] = rho_label
        
        ### END OF GREEKS ###
        
        # Export Report Button
        export_button = tk.Button(
            self,
            text="Export\nSensitivity Report",
            font=("Arial", 24, "bold"),
            bg="#f0f3f5",
            fg="#1f3044",
            width=20,
            height=2,
            command=self.export_report_cb 
        )   
        export_button.pack(pady=100)
        export_button.place(x=1000, y=600)
        """
        
