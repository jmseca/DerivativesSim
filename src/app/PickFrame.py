"""
Author: PMC
Date: 12 Nov 2024

Pick Frame definition

== Frame Explanation ==
Pick Frame is the frame where the user chooses the Derivative he/she wants to use
"""

import tkinter as tk

from AppRoot import AppRoot


class PickFrame(tk.Frame):
    
    id = "Pick"
    
    def __init__(self, root: AppRoot, geom: str):

        self.bg = "#97c5eb"
        super().__init__(root, bg=self.bg)
        self.root = root
        
    def vanilla_cb(self):
        
        """
        Callback for the "Option" button present on the welcome_frame
        
        It will hide PickFrame and show OptionFrame
        """
        from OptionFrame import OptionFrame
        
        self.root.hide(PickFrame.id)
        self.root.show(OptionFrame.vanilla_id)
        
    def exotic_cb(self):
        
        """
        Callback for the "Option" button present on the welcome_frame
        
        It will hide PickFrame and show OptionFrame
        """
        from OptionFrame import OptionFrame
        
        self.root.hide(PickFrame.id)
        self.root.show(OptionFrame.exotic_id)
        
        
    def build(self):
        
        # Add "Choose your derivative" text
        choose_der_txt = tk.Label(self, text="Choose your derivative", font=("Arial", 36, "bold"), fg="#1f3044", bg=self.bg)
        choose_der_txt.place(x=3,y=3)
        
        
        # Add Vanilla Option 
        vanilla_button = tk.Button(
            self,
            text="Option (Vanilla)",
            font=("Arial", 24),
            bg="#1f3044",
            fg="#f0f3f5",
            command=self.vanilla_cb 
        )   
        
        vanilla_button.pack(pady=100)
        
        # Center the button in the middle of the screen
        vanilla_button.place(x=50, y=100, width=400, height=70, anchor="nw")
        
        # Add Asset or Nothing
        exotic_button = tk.Button(
            self,
            text="Option (Asset/Nothing)",
            font=("Arial", 24),
            bg="#1f3044",
            fg="#f0f3f5",
            command=self.exotic_cb 
        )   
        
        exotic_button.pack(pady=100)
        
        # Center the button in the middle of the screen
        exotic_button.place(x=600, y=100, width=400, height=70, anchor="nw")
        
