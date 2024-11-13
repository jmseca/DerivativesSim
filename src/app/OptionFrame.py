"""
Author: PMC
Date: 12 Nov 2024

Option Frame definition

== Frame Explanation ==
Option Frame is where the user will input the values for its Option and get outputs
"""

import tkinter as tk

from AppRoot import AppRoot


class OptionFrame(tk.Frame):
    
    id = "Option"
    
    def __init__(self, root: AppRoot, geom: str):

        self.bg = "#97c5eb"
        super().__init__(root, bg=self.bg)
        self.root = root
        
    
    def go_back_cb(self):
        """
        Callback for the "Go back" button
        
        It will hide OptionFrame and show PickFrame
        """
        from PickFrame import PickFrame
        
        self.root.show(PickFrame.id)
        self.root.hide(OptionFrame.id)
    
        
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
        vanilla_option_txt = tk.Label(self, text="Option", font=("Arial", 36, "bold"), fg="#1f3044", bg=self.bg)
        vanilla_option_txt.place(x=0,y=100)
        
        ## INPUTS ##
        
        # Price 
        price_input = tk.Entry(self)
        price_input.place(x=0, y=200)
        
        # Strike Price 
        strike_input = tk.Entry(self)
        strike_input.place(x=0, y=250)
        
