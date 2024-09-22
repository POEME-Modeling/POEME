import tkinter as tk
  
class MoveCanvas(tk.Canvas):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.dx = 0
        self.dy = 0
  
        self.box = self.create_rectangle(0, 0, 10, 10, fill="black")
 
        self.dt = 25
        self.tick()
      
    def tick(self):
 
        self.move(self.box, self.dx, self.dy)
        self.after(self.dt, self.tick)
 
    def change_heading(self, dx, dy):
        self.dx = dx
        self.dy = dy
  
 
if __name__ == "__main__":
 
    root = tk.Tk()
    root.geometry("300x300")
 
    cvs = MoveCanvas(root)
    cvs.pack(fill="both", expand=True)
 
    ds = 3
  
    root.bind("<KeyPress-Left>", lambda _: cvs.change_heading(-ds, 0))
    root.bind("<KeyPress-Right>", lambda _: cvs.change_heading(ds, 0))
    root.bind("<KeyPress-Up>", lambda _: cvs.change_heading(0, -ds))
    root.bind("<KeyPress-Down>", lambda _: cvs.change_heading(0, ds))
      
    root.mainloop()