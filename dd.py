import tkinter as tk

def drag_pos(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def drag(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

root = tk.Tk()
#canvas = tk.Canvas(root, width=400, height=400)
#canvas.pack()

#rect = canvas.create_rectangle(10, 10, 50, 50, fill="blue")

canvas = tk.Canvas(root, width=200, height=200)

#square = Label( root, bg = "red", width=10, heigh = 5 )
#square.place( x=0, y=0 )


square = canvas.create_rectangle( 50, 50, 100, 100, fill="#ff0000")
square.bind( "<Button-1>", drag_pos)
square.bind("<B1-Motion>", drag)



square1 = Label( root, bg = "blue", width=10, heigh = 5 )
square1.place( x=0, y=0 )


square1.bind( "<Button-1>", drag_pos)
square1.bind("<B1-Motion>", drag)

create_line(15, 25, 200, 25)
root.mainloop()

canvas.tag_bind(rect, "<Button-1>", drag_start)
canvas.tag_bind(rect, "<B1-Motion>", drag_motion)



rect1 = canvas.create_rectangle(100, 100, 70, 70, fill="red")

canvas.tag_bind(rect1, "<Button-1>", drag_start)
canvas.tag_bind(rect1, "<B1-Motion>", drag_motion)

root.mainloop()