from tkinter import *
from tkinter import ttk, colorchooser

class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)
        self.coordinates_matrix = []  # initialize the matrix to store the coordinates
        self.first_coordinate = True  # flag to track whether this is the first coordinate in the stroke
        self.master.bind('<KeyPress>', self.on_key_press)
        self.current_coordinate = 0  # counter to track the current coordinate in the matrix

    def paint(self, e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.penwidth, fill=self.color_fg, capstyle=ROUND, smooth=True)

        # update the coordinates matrix with the current coordinates
        self.coordinates_matrix.append([e.x, self.c.winfo_height() - e.y])

        self.old_x = e.x
        self.old_y = e.y
        self.coordinates['text'] = f'X: {e.x} Y: {self.c.winfo_height() - e.y}'

    def reset(self, e):
        # add 69420 for both X and Y when the pen stroke ends
        self.coordinates_matrix.append([100000, 100000])

        self.old_x = None
        self.old_y = None
        self.coordinates['text'] = ''

    def on_key_press(self, e):
        if e.char == ' ':
            self.normalize_coordinates()
            print(self.coordinates_matrix)
            self.save_coordinates()
    
    def normalize_coordinates(self):
        # find the minimum X and Y values
        min_x = min(coord[0] for coord in self.coordinates_matrix)
        min_y = min(coord[1] for coord in self.coordinates_matrix)

        # subtract the minimum X and Y values from all values in the matrix
        for coord in self.coordinates_matrix:
            coord[0] -= min_x
            coord[1] -= min_y

    def save_coordinates(self):
        # open the file in write mode
        with open("TestFont.txt", "w") as f:
            # write "U" before the first coordinate
            f.write("U\n")
            for coord in self.coordinates_matrix:
                if self.first_coordinate:
                    f.write(f"{coord[0]} {coord[1]}\n")
                    self.current_coordinate += 1
                    f.write("D\n")
                    self.first_coordinate = False
                if coord[0] > 20000 or coord[1] > 20000:
                    f.write("U\n")
                    self.first_coordinate = True
                else:
                    f.write(f"{coord[0]} {coord[1]}\n")
                self.current_coordinate += 1


    def changeW(self,e): #change Width of pen through slider
        self.penwidth = e
           

    def clear(self):
        self.c.delete(ALL)

    def drawWidgets(self):
        self.controls = Frame(self.master,padx = 5,pady = 5)
        self.clear_btn = Button(self.controls, text='Clear Canvas', command=self.clear)
        self.clear_btn.grid(row=0,column=0)
        self.coordinates = Label(self.controls, text='')
        self.coordinates.grid(row=1,column=0)
        Label(self.controls, text='Pen Width:',font=('arial 18')).grid(row=2,column=0)
        self.slider = ttk.Scale(self.controls,from_= 5, to = 100,command=self.changeW,orient=VERTICAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=2,column=1,ipadx=30)
        self.controls.pack(side=LEFT)
        
        self.c = Canvas(self.master,width=500,height=400,bg=self.color_bg,)
        self.c.pack(fill=BOTH,expand=True)



if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Application')
    root.mainloop() 