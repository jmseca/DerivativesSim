

import tkinter as tk


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
    
    geom = "1200x600"
    
    # Init App 
    app = AppRoot(geom)
    
    # Init all the frames
    welcome_frame = WelcomeFrame(app, geom)
    pick_frame = PickFrame(app, geom)
    
    
    # Add all the frames to the App
    app.add_frame(WelcomeFrame.id, welcome_frame)
    app.add_frame(PickFrame.id,pick_frame)
    
    # Build all the frames
    welcome_frame.build()
    pick_frame.build()
    
    # Run App
    app.show(WelcomeFrame.id)
    app.mainloop()