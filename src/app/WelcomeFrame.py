"""
Author: PMC
Date: 12 Nov 2024

Wellcome Frame definition

== Frame Explanation ==
Wellcome Frame is the first app frame shown to users, with the PMC background and a "Get Started" button
"""

import tkinter as tk
from PIL import Image, ImageTk

from AppRoot import AppRoot
from PickFrame import PickFrame


class WelcomeFrame(tk.Frame):
    
    id = "Welcome"
    
    def __init__(self, root: AppRoot, geom: str):

        super().__init__(root, bg="white")
        self.root = root
        
    def get_started_cb(self):
        
        """
        Callback for the "Get Started" button present on the welcome_frame
        
        It will hide welcome_frame and show pick_frame
        """
        
        self.root.hide(WelcomeFrame.id)
        self.root.show(PickFrame.id)
        
    def build(self):
        
        # Add PMC background
        #background_image = Image.open("pmc.png")  # Replace with your image file name
        #background_photo = ImageTk.PhotoImage(background_image)
        #print("I was here")

        #background_label = tk.Label(self, image=background_photo)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        bg = tk.PhotoImage(file = "pmc.png")
        label1 = tk.Label( self, image = bg) 
        label1.img = bg
        label1.place(x = 0, y = 0) 
        
                
        # Create "Get Started" button
        get_started_button = tk.Button(
            self,
            text="Get Started",
            font=("Arial", 16),
            bg="blue",
            fg="black",
            command=self.get_started_cb  # Call function to show the CR7 frame
        )   
        
        get_started_button.pack(pady=100)
        
        # Center the button in the middle of the screen
        get_started_button.place(relx=0.5, rely=0.5, anchor="center")
