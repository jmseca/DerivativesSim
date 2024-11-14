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
from option_pricing import option_price, delta, gamma, rho, vega

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
    gamma = "gamma"
    vega = "vega"
    rho = "rho"
    
    def __init__(self, root: AppRoot, geom: str, vtype: VisualType):

        self.bg = "#97c5eb"
        
        super().__init__(root, bg=self.bg)
        self.fg = "#1f3044"
        self.root = root
        self.visual_type = vtype
        #self.built = -1
        self.slider_labels = "Volatility" if vtype is VisualType.Vol else "Maturity (yrs)" if vtype is VisualType.Mat else "Risk-free rate"
        self.scale_max = 5 if vtype is VisualType.Mat else 1
        
        self.plt_col = "blue" if vtype is VisualType.Vol else "green" if vtype is VisualType.Mat else "red"
        
        
        
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
        
        # I only need to build the frames on the Right CB
        
        if self.visual_type is VisualType.Mat:
            rf_frame = self.root.get_frame(VisualFrame.rf_id)
            rf_frame.build(self.vanilla, self.option)
            self.root.show(VisualFrame.rf_id)
            self.root.hide(VisualFrame.mat_id)
        elif self.visual_type is VisualType.Vol:
            mat_frame = self.root.get_frame(VisualFrame.mat_id)
            mat_frame.build(self.vanilla, self.option)
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
            
            y_values = option_price(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                val, 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        elif self.visual_type is VisualType.Vol:
            
            y_values = option_price(
                self.x_values,
                self.option.strike,
                val,
                self.option.get_years_to_maturity(), 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        else:
            
            y_values = option_price(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                self.option.get_years_to_maturity(), 
                val,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        self.lines[VisualFrame.price].set_ydata(y_values)
        self.canvas[VisualFrame.price].draw()
        
        
    def update_delta(self, val):
        
        val = float(val)
        
        if self.visual_type is VisualType.Mat:
            
            y_values = delta(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                val, 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        elif self.visual_type is VisualType.Vol:
            
            y_values = delta(
                self.x_values,
                self.option.strike,
                val,
                self.option.get_years_to_maturity(), 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        else:
            
            y_values = delta(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                self.option.get_years_to_maturity(), 
                val,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        self.lines[VisualFrame.delta].set_ydata(y_values)
        self.canvas[VisualFrame.delta].draw()
        
        
    def update_gamma(self, val):
        
        val = float(val)
        
        if self.visual_type is VisualType.Mat:
            
            y_values = gamma(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                val, 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        elif self.visual_type is VisualType.Vol:
            
            y_values = gamma(
                self.x_values,
                self.option.strike,
                val,
                self.option.get_years_to_maturity(), 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        else:
            
            y_values = gamma(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                self.option.get_years_to_maturity(), 
                val,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        self.lines[VisualFrame.gamma].set_ydata(y_values)
        self.canvas[VisualFrame.gamma].draw()
        
        
    def update_vega(self, val):
        
        val = float(val)
        
        if self.visual_type is VisualType.Mat:
            
            y_values = vega(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                val, 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        elif self.visual_type is VisualType.Vol:
            
            y_values = vega(
                self.x_values,
                self.option.strike,
                val,
                self.option.get_years_to_maturity(), 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        else:
            
            y_values = vega(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                self.option.get_years_to_maturity(), 
                val,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        self.lines[VisualFrame.vega].set_ydata(y_values)
        self.canvas[VisualFrame.vega].draw()
        
        
    def update_rho(self, val):
        
        val = float(val)
        
        if self.visual_type is VisualType.Mat:
            
            y_values = rho(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                val, 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        elif self.visual_type is VisualType.Vol:
            
            y_values = rho(
                self.x_values,
                self.option.strike,
                val,
                self.option.get_years_to_maturity(), 
                self.option.free_rate,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        else:
            
            y_values = rho(
                self.x_values,
                self.option.strike,
                self.option.annual_vol,
                self.option.get_years_to_maturity(), 
                val,
                self.option.div_yield,
                self.vanilla,
                self.option.is_call()
            )
            
        self.lines[VisualFrame.rho].set_ydata(y_values)
        self.canvas[VisualFrame.rho].draw()
        
        
    def build(self, vanilla: bool, option: Option):
        
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
        # Title
        title_txt = tk.Label(self, text=self.slider_labels, font=("Arial", 40, "bold", "underline"), fg=self.fg, bg=self.bg)
        title_txt.place(x=600,y=10)
        
        ########### GRAPHS ###########
        
        # Option Price
        
        price_fig, price_ax = plt.subplots(figsize=(4, 2.5))
        price_y = option_price(
            self.x_values,
            self.option.strike,
            self.option.annual_vol,
            self.option.get_years_to_maturity(), 
            self.option.free_rate,
            self.option.div_yield,
            self.vanilla,
            self.option.is_call()
        )
        price_line, = price_ax.plot(self.x_values, price_y, lw=2, color=self.plt_col)
        self.lines[VisualFrame.price] = price_line
        price_ax.set_title("Option Price as function of Asset Price")
        price_ax.set_xlabel("Asset Price")
        price_ax.set_ylabel("Option Price")
        price_fig.tight_layout()
        
        price_canvas = FigureCanvasTkAgg(price_fig, master=self)
        price_canvas.get_tk_widget().place(x=50,y=100, width=400)
        self.canvas[VisualFrame.price] = price_canvas
        
        price_vol_slider = tk.Scale(self, from_=0, to=self.scale_max, orient="horizontal", label=self.slider_labels, resolution=0.01, command=self.update_price)
        price_vol_slider.set(self.option.annual_vol)
        price_vol_slider.place(x=50, y=350)
        price_vol_slider.config(length=400)
        
        
        # Option Delta 
        
        delta_fig, delta_ax = plt.subplots(figsize=(4, 2.5))
        delta_y = delta(
            self.x_values,
            self.option.strike,
            self.option.annual_vol,
            self.option.get_years_to_maturity(), 
            self.option.free_rate,
            self.option.div_yield,
            self.vanilla,
            self.option.is_call()
        )
        delta_line, = delta_ax.plot(self.x_values, delta_y, lw=2, color=self.plt_col)
        self.lines[VisualFrame.delta] = delta_line
        delta_ax.set_title("Option Delta as function of Asset Price")
        delta_ax.set_xlabel("Asset Price")
        delta_ax.set_ylabel("Option Delta")
        delta_fig.tight_layout()
        
        delta_canvas = FigureCanvasTkAgg(delta_fig, master=self)
        delta_canvas.get_tk_widget().place(x=500,y=100, width=400)
        self.canvas[VisualFrame.delta] = delta_canvas
        
        delta_slider = tk.Scale(self, from_=0, to=self.scale_max, orient="horizontal", label=self.slider_labels, resolution=0.01, command=self.update_delta)
        delta_slider.set(self.option.annual_vol)
        delta_slider.place(x=500, y=350)
        delta_slider.config(length=400)
        
        # Option Gamma 
        
        gamma_fig, gamma_ax = plt.subplots(figsize=(4, 2.5))
        gamma_y = gamma(
            self.x_values,
            self.option.strike,
            self.option.annual_vol,
            self.option.get_years_to_maturity(), 
            self.option.free_rate,
            self.option.div_yield,
            self.vanilla,
            self.option.is_call()
        )
        gamma_line, = gamma_ax.plot(self.x_values, gamma_y, lw=2, color=self.plt_col)
        self.lines[VisualFrame.gamma] = gamma_line
        gamma_ax.set_title("Option Gamma as function of Asset Price")
        gamma_ax.set_xlabel("Asset Price")
        gamma_ax.set_ylabel("Option Gamma")
        gamma_fig.tight_layout()
        
        gamma_canvas = FigureCanvasTkAgg(gamma_fig, master=self)
        gamma_canvas.get_tk_widget().place(x=950,y=100, width=400)
        self.canvas[VisualFrame.gamma] = gamma_canvas
        
        gamma_slider = tk.Scale(self, from_=0, to=self.scale_max, orient="horizontal", label=self.slider_labels, resolution=0.01, command=self.update_gamma)
        gamma_slider.set(self.option.annual_vol)
        gamma_slider.place(x=950, y=350)
        gamma_slider.config(length=400)
        
        
        # Option Vega 
        
        vega_fig, vega_ax = plt.subplots(figsize=(4, 2.5))
        vega_y = vega(
            self.x_values,
            self.option.strike,
            self.option.annual_vol,
            self.option.get_years_to_maturity(), 
            self.option.free_rate,
            self.option.div_yield,
            self.vanilla,
            self.option.is_call()
        )
        vega_line, = vega_ax.plot(self.x_values, vega_y, lw=2, color=self.plt_col)
        self.lines[VisualFrame.vega] = vega_line
        vega_ax.set_title("Option Vega as function of Asset Price")
        vega_ax.set_xlabel("Asset Price")
        vega_ax.set_ylabel("Option Vega")
        vega_fig.tight_layout()
        
        vega_canvas = FigureCanvasTkAgg(vega_fig, master=self)
        vega_canvas.get_tk_widget().place(x=50,y=450, width=400)
        self.canvas[VisualFrame.vega] = vega_canvas
        
        vega_slider = tk.Scale(self, from_=0, to=self.scale_max, orient="horizontal", label=self.slider_labels, resolution=0.01, command=self.update_vega)
        vega_slider.set(self.option.annual_vol)
        vega_slider.place(x=50, y=700)
        vega_slider.config(length=400)
        
        
    # Option Rho 
        
        rho_fig, rho_ax = plt.subplots(figsize=(4, 2.5))
        rho_y = rho(
            self.x_values,
            self.option.strike,
            self.option.annual_vol,
            self.option.get_years_to_maturity(), 
            self.option.free_rate,
            self.option.div_yield,
            self.vanilla,
            self.option.is_call()
        )
        rho_line, = rho_ax.plot(self.x_values, rho_y, lw=2, color=self.plt_col)
        self.lines[VisualFrame.rho] = rho_line
        rho_ax.set_title("Option Rho as function of Asset Price")
        rho_ax.set_xlabel("Asset Price")
        rho_ax.set_ylabel("Option Rho")
        rho_fig.tight_layout()
        
        rho_canvas = FigureCanvasTkAgg(rho_fig, master=self)
        rho_canvas.get_tk_widget().place(x=500,y=450, width=400)
        self.canvas[VisualFrame.rho] = rho_canvas
        
        rho_slider = tk.Scale(self, from_=0, to=self.scale_max, orient="horizontal", label=self.slider_labels, resolution=0.01, command=self.update_rho)
        rho_slider.set(self.option.annual_vol)
        rho_slider.place(x=500  , y=700)
        rho_slider.config(length=400)
        
        
        ### END OF GRAPHS ###
        
        # Add Go Right Button
        go_right_button = tk.Button(
            self,
            text=">",
            font=("Arial", 24),
            bg="light grey",
            fg="#1f3044",
            command=self.go_right_cb 
        )   
        
        
        if not(self.visual_type is VisualType.Rf):
            go_right_button.place(x=1550,y=750,width=50,height=50)
        
        # Add Go Left Button
        go_left_button = tk.Button(
            self,
            text="<",
            font=("Arial", 24),
            bg="light grey",
            fg="#1f3044",
            command=self.go_left_cb 
        )   
        
        
        if not(self.visual_type is VisualType.Vol):
            go_left_button.place(x=1500,y=750,width=50,height=50)