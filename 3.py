from tkinter import Tk, Frame, Canvas, CURRENT, Text, END, TRUE, BOTH

click = 0

def drag_pos(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def drag(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
    widget.feature_xpos = x

class features_object():
    
    def __init__(self, master, feature_text, feature_xpos, feature_ypos, feature_color):

        self.master = master
        self.feature_text = feature_text
        self.feature_xpos = feature_xpos
        self.feature_ypos = feature_ypos
        self.feature_color = feature_color

        self.click = 0
        
        self.feature_frame = Frame(self.master, bg=self.feature_color, border=40)   
        self.feature_text = Text(self.feature_frame, font=("Helvetica", 12), relief='flat', width=20, height=3, selectbackground=self.feature_color, selectforeground="black", exportselection=TRUE)
        self.feature_text.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.feature_text.config(wrap='word')
        self.feature_text.insert(END, feature_text)
        self.feature_tags = 'feature'
        self.feature_id = self.master.create_window(self.feature_xpos, self.feature_ypos, window=self.feature_frame, tags=self.feature_tags)


        self.bind_events()

    def bind_events(self):
        self.feature_frame.bind('<Button-2>', self.clicked)
        self.feature_frame.bind('<Button-2>', self.draw_line_with_bind)
        self.feature_frame.bind( "<Button-1>", drag_pos)
        self.feature_frame.bind("<B1-Motion>", drag)





    def clicked(self, event=None):
        print('You clicked {self.feature_id} with the cords {self.master.coords(self.feature_id)}')

    def draw_line_with_bind(self, event):
        global click,start_x,start_y,end_x,end_y
        
        self.activ_elem = self.master.coords(self.feature_id)
        
        if click == 0:
            self.elem_start = self.activ_elem
            start_x = self.activ_elem[0]
            start_y = self.activ_elem[1]
            start_x= self.feature_xpos
            click = 1 
            
            
            
        elif click == 1:
            self.elem_end = self.activ_elem
            end_x = self.activ_elem[0]
            end_y = self.activ_elem[1]
            self.master.create_line(start_x, start_y, end_x, end_y, fill="red", width=5)
            click = 0 


window = Tk()
window.geometry("1000x800")

frame_start = Frame(window)
frame_start.pack(expand=TRUE, fill=BOTH)

draw_canvas = Canvas(frame_start)
draw_canvas.pack(expand=TRUE, fill=BOTH)

created_feature_1 = features_object(draw_canvas, 'feature A', 100, 100, 'red')
created_feature_2 = features_object(draw_canvas, 'feature B', 300, 300, 'green')
created_feature_3 = features_object(draw_canvas, 'feature C', 500, 500, 'magenta')


if __name__ == '__main__':
    window.mainloop()