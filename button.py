from tkinter import *   
    
win = Tk()  ## win is a top or parent window
  
win.geometry("200x100")  
  
b = Button(win, text = "Submit")  
  
b.pack()  #using pack() geometry
  
win.mainloop()  