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

from AppRoot import AppRoot
from options import Option, Period, OptionType, OptionStyle


class OptionFrame(tk.Frame):
    
    vanilla_id = "Vanilla"
    exotic_id = "Exotic"
    
    # Inputs IDs
    s0 = "value"
    strike = "strike"
    period_size = "period_size"
    maturity = "maturity"
    vol = "volatility"
    frate = "free rate"
    div = "dividend yield"
    option_type = "option_type"
    style = "option_style"
    error = "error"
    
    # Outputs IDs
    price_label = "price_label"
    delta_label = "delta_label"
    gamma_label = "gamma_label"
    vega_label  = "vega_label"
    rho_label = "rho_label"
    
    
    def __init__(self, root: AppRoot, geom: str, vanilla: bool,  option: Option):

        self.bg = "#97c5eb"
        
        super().__init__(root, bg=self.bg)
        self.fg = "#1f3044"
        self.root = root
        self.vanilla = vanilla
        self.option = option
        self.inputs = {}
        self.outputs = {}
        
        self.greeks_round = 3
        
    
    def go_back_cb(self):
        """
        Callback for the "Go back" button
        
        It will hide OptionFrame and show PickFrame
        """
        from PickFrame import PickFrame
        
        self.root.show(PickFrame.id)
        if self.vanilla:
            self.root.hide(OptionFrame.vanilla_id)
        else:
            self.root.hide(OptionFrame.exotic_id)
    
    def set_period_cb(self):
        """
        Sets the option period_size, everytime the user changes the values
        """
        period_size = Period.Months if (self.inputs[OptionFrame.period_size].get()==1) else Period.Years
        self.option.period_size = period_size
        
    def set_type_cb(self):
        """
        Sets the option type (Call/Put), everytime the user changes the values
        """
        option_type = OptionType.Call if (self.inputs[OptionFrame.option_type].get()==1) else OptionType.Put
        self.option.option_type = option_type
   
    def price_it_cb(self):
        
        # Get User Inputs
        usr_s0 = self.inputs[OptionFrame.s0].get()
        usr_strike = self.inputs[OptionFrame.strike].get()
        usr_maturity = self.inputs[OptionFrame.maturity].get()
        usr_vol = self.inputs[OptionFrame.vol].get()
        usr_div = self.inputs[OptionFrame.div].get()
        usr_frate = self.inputs[OptionFrame.frate].get()
        
        # Period_Size, Type, and Style are automatically set
        # Try to change option values
        erro_tag = self.inputs[OptionFrame.error]
        try:
            self.option.set_s0(usr_s0)
            self.option.set_strike(usr_strike)
            self.option.set_maturity(usr_maturity)
            self.option.set_volatility(usr_vol)
            self.option.set_free_rate(usr_frate)
            self.option.set_div_yiled(usr_div)
            
            # If here, all values were valid
            erro_tag.place_forget()
            
            # Change Price + Greeks
            price_label = self.outputs[OptionFrame.price_label]
            price_label.config(text=f"{round(self.option.price(),2)} €")
            delta_label = self.outputs[OptionFrame.delta_label]
            delta_label.config(text=f"{round(self.option.delta(),self.greeks_round)}")
            gamma_label = self.outputs[OptionFrame.gamma_label]
            gamma_label.config(text=f"{round(self.option.gamma(),self.greeks_round)}")
            vega_label = self.outputs[OptionFrame.vega_label]
            vega_label.config(text=f"{round(self.option.vega(),self.greeks_round)}")
            rho_label = self.outputs[OptionFrame.rho_label]
            rho_label.config(text=f"{round(self.option.rho(),self.greeks_round)}")
                        
        except Exception as e:
            # In case of error, show it to the User
            erro_tag.config(text=str(e))
            erro_tag.place(x=50, y=470)

            
            
    def visualise_cb(self):
    
        from VisualFrame import VisualFrame
        
        vol_frame = self.root.get_frame(VisualFrame.vol_id)
        vol_frame.build(self.vanilla, self.option)
        
        self.root.show(VisualFrame.vol_id)
        if self.vanilla:
            self.root.hide(OptionFrame.vanilla_id)
        else:
            self.root.hide(OptionFrame.exotic_id)
        
        
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
        
        
        txt_value = "Vanilla Option" if self.vanilla else "Asset-Or-Nothing Option"
        
        option_txt = tk.Label(self, text=txt_value, font=("Arial", 36, "bold"), fg=self.fg, bg=self.bg)
        option_txt.place(x=0,y=100)
        
        ########### INPUTS ###########
        
        input_x_offset = 300
        
        # S0 
        s0_tag = tk.Label(self, text="Current Asset Price (€)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        s0_tag.place(x=50, y=200)
        
        s0_input = tk.Entry(self,justify="right")
        s0_input.insert(0, str(self.option.s0))
        s0_input.place(x=input_x_offset, y=200)
        # Add it to inputs
        self.inputs[OptionFrame.s0] = s0_input
        
        # Strike Price 
        strike_tag = tk.Label(self, text="Strike Price (€)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        strike_tag.place(x=50, y=230)
        
        strike_input = tk.Entry(self,justify="right")
        strike_input.insert(0, str(self.option.strike))
        strike_input.place(x=input_x_offset, y=230)
        # Add it to inputs
        self.inputs[OptionFrame.strike] = strike_input
        
        # Period Size
        period_tag = tk.Label(self, text="Period Size", font=("Arial", 14), fg=self.fg, bg=self.bg)
        period_tag.place(x=50, y=260)
        
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
        maturity_tag.place(x=50, y=290)
        
        maturity_input = tk.Entry(self,justify="right")
        maturity_input.insert(0, str(self.option.maturity))
        maturity_input.place(x=input_x_offset, y=290)
        # Add it to inputs
        self.inputs[OptionFrame.maturity] = maturity_input
        
        # Annual Volatility 
        vol_tag = tk.Label(self, text="Annual Volatility (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        vol_tag.place(x=50, y=320)
        
        vol_input = tk.Entry(self,justify="right")
        vol_input.insert(0, self.option.get_vol_str_perc()[:-2]) # Remove % sign
        vol_input.place(x=input_x_offset, y=320)
        # Add it to inputs
        self.inputs[OptionFrame.vol] = vol_input
        
        # Risk-free Rate 
        frate_tag = tk.Label(self, text="Risk-free rate (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        frate_tag.place(x=50, y=350)
        
        frate_input = tk.Entry(self,justify="right")
        frate_input.insert(50, self.option.get_frate_str_perc()[:-2]) # Remove % sign
        frate_input.place(x=input_x_offset, y=350)
        # Add it to inputs
        self.inputs[OptionFrame.frate] = frate_input
        
        
        # Dividend Yield 
        div_tag = tk.Label(self, text="Annual Dividend Yield (%)", font=("Arial", 14), fg=self.fg, bg=self.bg)
        div_tag.place(x=50, y=380)
        
        div_input = tk.Entry(self,justify="right")
        div_input.insert(0, self.option.get_div_yield_str_perc()[:-2]) # Remove % sign
        div_input.place(x=input_x_offset, y=380)
        # Add it to inputs
        self.inputs[OptionFrame.div] = div_input
        
        # Option Type
        type_tag = tk.Label(self, text="Option Type", font=("Arial", 14), fg=self.fg, bg=self.bg)
        type_tag.place(x=50, y=410)
        
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
        
        delta_label = tk.Label(self, text=f"{round(self.option.delta(),self.greeks_round)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        delta_label.place(x=1000, y=310, width=300, height=35)
        self.outputs[OptionFrame.delta_label] = delta_label
        
        # Gamma
        gamma_tag = tk.Label(self, text="Gamma", font=("Arial", 18, "bold"), fg=self.fg, bg=self.bg)
        gamma_tag.place(x=1000, y=350)
        
        gamma_label = tk.Label(self, text=f"{round(self.option.gamma(),self.greeks_round)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        gamma_label.place(x=1000, y=380, width=300, height=35)
        self.outputs[OptionFrame.gamma_label] = gamma_label
        
        # Vega
        vega_tag = tk.Label(self, text="Vega", font=("Arial", 18, "bold"), fg=self.fg, bg=self.bg)
        vega_tag.place(x=1000, y=420)
        
        vega_label = tk.Label(self, text=f"{round(self.option.vega(),self.greeks_round)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        vega_label.place(x=1000, y=450, width=300, height=35)
        self.outputs[OptionFrame.vega_label] = vega_label
        
        # Rho
        rho_tag = tk.Label(self, text="Rho", font=("Arial", 18, "bold"), fg=self.fg, bg=self.bg)
        rho_tag.place(x=1000, y=490)
        
        rho_label = tk.Label(self, text=f"{round(self.option.rho(),self.greeks_round)}", font=("Arial", 18, "bold"),
            fg=self.fg, bg="light grey", anchor="e")
        rho_label.place(x=1000, y=520, width=300, height=35)
        self.outputs[OptionFrame.rho_label] = rho_label
        
        ### END OF GREEKS ###
        
        # Export Report Button
        visualize_button = tk.Button(
            self,
            text="Visualize Risk",
            font=("Arial", 24, "bold"),
            bg="#f0f3f5",
            fg="#1f3044",
            width=20,
            height=2,
            command=self.visualise_cb 
        )   
        visualize_button.pack(pady=100)
        visualize_button.place(x=1000, y=600)
        
        
