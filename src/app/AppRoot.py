

import tkinter as tk

import os
import sys
sys.path.append("../derivatives/")

from options import Option, VanillaOption, AssetOrNothinOption


class AppRoot(tk.Tk):
    
    def __init__(self, geom: str):
        
        super().__init__()
        self.title("PMC Simulation Tool")
        self.geometry(geom)
        self.resizable(False, False)
        
        self.frames = {}
        
    def add_frame(self, id: str, frame: tk.Tk):
        
        if id not in self.frames:
            self.frames[id] = frame
        
        
    def show(self, frame_id: str):
        
        frame = self.frames[frame_id]
        frame.pack(fill="both", expand=True)
        frame.tkraise()
        
        
        
    def hide(self, frame_id: str):
        
        frame = self.frames[frame_id]
        frame.pack_forget()
        
        
        

if __name__ == "__main__":
    
    from WelcomeFrame import WelcomeFrame
    from PickFrame import PickFrame
    from OptionFrame import OptionFrame
    
    geom = "1600x800"
    
    # Init App 
    app = AppRoot(geom)
    
    # Init all the frames
    welcome_frame = WelcomeFrame(app, geom)
    pick_frame = PickFrame(app, geom)
    vanilla_frame = OptionFrame(app, geom, True, VanillaOption())
    exotic_frame = OptionFrame(app, geom, False, AssetOrNothinOption())
    
    
    # Add all the frames to the App
    app.add_frame(WelcomeFrame.id, welcome_frame)
    app.add_frame(PickFrame.id, pick_frame)
    app.add_frame(OptionFrame.vanilla_id, vanilla_frame)
    app.add_frame(OptionFrame.exotic_id, exotic_frame)
    
    # Build all the frames
    welcome_frame.build()
    pick_frame.build()
    vanilla_frame.build()
    exotic_frame.build()
    
    # Run App
    app.show(WelcomeFrame.id)
    app.mainloop()