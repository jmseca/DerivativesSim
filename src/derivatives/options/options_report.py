"""
Author: PMC
Date: 12 Nov 2024

Definition of Option Report functions
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet


from option_pricing import black_scholes

class OptionReport:
    
    """
    OptionReport Class
    
    Each object will be able to create a Report of the Option stored as an attribute.
    This report will consist of:
    
    - Volatility Sensitivity
    - Strike Price Sensitivity
    - Risk-free rate Sensitivity
    """
    
    doc_destination = "../../reports/"
    img_temp_destination = "../../media/temp/"
    
    def __init__(self, fname: str, option):
        
        self.option = option
        self.fname = OptionReport.doc_destination + fname + ".pdf"
        self.doc = SimpleDocTemplate(self.fname, pagesize=letter)
        self.style = getSampleStyleSheet()
        self.elements = []
        self.small_spacer = Spacer(1, 12)
        self.big_spacer = Spacer(1, 24)
        
        self.default_std_for_sensitivity = 0.3  #30%
        self.default_size_for_sensitivity = 100
        
    def save_plot(self, x: list, y: list, x_label: str, y_label: str, fname: str, title: str, color: str):
        
        # Create Plot
        plt.figure(figsize=(5, 3))
        plt.plot(x, y, color=color)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
        # I only want 5 xticks
        plt.xticks(np.linspace(x[0], x[-1], 5)) 
        plt.tight_layout()
        
        # Save it
        print(os.getcwd())
        print("Saved plot in ",OptionReport.img_temp_destination+fname+'.png')
        plt.savefig(OptionReport.img_temp_destination+fname+'.png')
        plt.close()
        
        
    def write_plot(self, fname: str):

        # Can Change Width and Height 
        Width = 500
        Height = 300
        self.elements.append(Image(
                OptionReport.img_temp_destination+fname+'.png', # file destination
                width=Width,
                height=Height
            ))
        self.elements.append(self.big_spacer)
        
        
        
        
    def write_bullet_points(self, **info):
        """
        Adds the bullet points to self.elements
        """      
        for key, value in info.items():
            
            # Keys_Will_Be_Like_This (but we want Keys Like This)
            key_spaced = key.replace("_"," ")
            
            point = f"<b>{key_spaced}</b>:\t\t\t\t{value}"
            self.elements.append(Paragraph(f"• {point}", self.style['Normal']))
            
        
        # Add a Spacer in the end
        self.elements.append(self.small_spacer)
            
            
    def write_intro(self):
        
        # Add Title
        self.elements.append(Paragraph("PMC Option Report", self.style["Title"]))
        self.elements.append(self.small_spacer)
        
        # Add Option features
        self.elements.append(Paragraph("Option Features", self.style["Heading2"]))
        self.write_bullet_points(
            Underlying_Value    = self.option.s0,
            Strike_Price        = self.option.strike,
            Years_to_Maturity   = self.option.get_years_to_maturity(),
            Annual_Volatility   = self.option.get_vol_str_perc(),
            Risk_Free_Rate      = self.option.get_frate_str_perc(),
            Dividend_Yield      = self.option.get_div_yield_str_perc(),
            Style               = self.option.get_option_style(),
            Type                = self.option.get_option_type()
        )
        self.elements.append(PageBreak())
        
        
    def write_vol_risk(self):
        """
        Writes the section dedicated to the volatility Sensitivity Analysis
        """
        vol = self.option.annual_vol
        std = self.default_std_for_sensitivity
        size = self.default_size_for_sensitivity
        graph_fname = "vol_sens"
        
        x_values = list(np.linspace((1-std)*vol, (1+std)*vol, size))
        
        op2 = self.option.copy()
        y_values = []
        
        for new_vol in x_values:
            
            op2.annual_vol = new_vol
            y_values += [op2.price()]
        
        # Add the section Title
        self.elements.append(Paragraph("Volatility Sensitivity", self.style["Heading2"]))
        
        # Add the Plot
        self.save_plot(x_values, y_values, "Volatility", "Option Price",
            graph_fname, "Price Sensitivity with Volatility","green")
        self.write_plot(graph_fname)
        
        # Add a Page Break
        self.elements.append(PageBreak())
        
        
        
    def write_strike_risk(self):
        """
        Writes the section dedicated to the volatility Sensitivity Analysis
        """
        strike = self.option.strike
        std = self.default_std_for_sensitivity
        size = self.default_size_for_sensitivity
        graph_fname = "strike_sens"
        
        x_values = list(np.linspace((1-std)*strike, (1+std)*strike, size))
        
        # y_values will contain the prices with changing strike prices
        y_values = []
        # Lets use a dummy option to get its price
        op2 = self.option.copy()
        
        for new_strike in x_values:
            op2.strike = new_strike
            y_values += [op2.price()]
        
        # Add the section Title
        self.elements.append(Paragraph("Strike Price Sensitivity", self.style["Heading2"]))
        
        # Add the Plot
        self.save_plot(x_values, y_values, "Strike Price", "Option Price",
            graph_fname, "Price Sensitivity with Strike Price","blue")
        self.write_plot(graph_fname)
        
        # Add a Page Break
        self.elements.append(PageBreak())
        
        
    def write_free_rate_risk(self):
        """
        Writes the section dedicated to the volatility Sensitivity Analysis
        """
        from option import OptionType
        
        frate = self.option.free_rate
        std = self.default_std_for_sensitivity
        size = self.default_size_for_sensitivity
        graph_fname = "frate_sens"
        
        x_values = list(np.linspace((1-std)*frate, (1+std)*frate, size))
        y_values = list(map(
            lambda new_frate : black_scholes(
                self.option.s0,
                self.option.strike,
                self.option.annual_vol,
                self.option.get_years_to_maturity(),
                new_frate,
                self.option.div_yield,
                call = self.option.option_type is OptionType.Call    
            ),
            x_values
        ))
        
        # Add the section Title
        self.elements.append(Paragraph("Risk-free Rate Sensitivity", self.style["Heading2"]))
        
        # Add the Plot
        self.save_plot(x_values, y_values, "Risk-Free Rate", "Option Price",
            graph_fname, "Price Sensitivity with Risk-Free Rate","red")
        self.write_plot(graph_fname)
        
        # Add a Page Break
        self.elements.append(PageBreak())
        
        
        
        
    def export(self):
        
        # First, write everything
        self.write_intro()
        self.write_vol_risk()
        self.write_strike_risk()
        self.write_free_rate_risk()
        
        # Then build the document
        self.doc.build(self.elements)
        
        
