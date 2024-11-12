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

        super().__init__(root, bg="blue")
        self.root = root
        
        
    def build(self):
        pass
        
