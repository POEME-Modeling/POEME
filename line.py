import tkinter as tk
import random

def connect(a,b):
    # compupte the tag, then delete any existing lines
    # between these two objects
    tag = f"connector_{a}_{b}"
    canvas.delete(tag)

    ax0, ay0, ax1, ay1 = canvas.coords(a)
    bx0, by0, bx1, by1 = canvas.coords(b)

    x0 = (ax0 + ax1) / 2
    y0 = (ay0 + ay1) / 2

    x1 = (bx0 + bx1) / 2
    y1 = (by0 + by1) / 2

    # create the line, then lower it below all other
    # objects
    line_id = canvas.create_line(x0, y0, x1, y1, fill="blue", width=4, tags=(tag,))
    canvas.tag_lower(line_id)

def move_rectangles():
    canvas.move(f1, random.randint(-50, 50), 0)
    canvas.move(f2, 0, random.randint(-50, 50))
    connect(f1, f2)

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=500, background="white")
button = tk.Button(root, text="Move rectangles", command=move_rectangles)

button.pack(side="top")
canvas.pack(side="top", fill="both", expand=True)

f1 = canvas.create_rectangle(50,50, 150, 250, outline="red", fill="white", width=4)
f2 = canvas.create_rectangle(250,100, 350, 350, outline="green", fill="white", width=4)

connect(f1, f2)


root.mainloop()