from Tkinter import *
from tkFileDialog import askopenfilename
import matplotlib import pyplot as plt

# some predefines
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 300
CANVAS_WIDTH = WINDOW_WIDTH
CANVAS_HEIGHT = 100
ERR_MSG = "Error!"

def callback():
    print "called the callback!"

def openfiledialog():
    name = askopenfilename()
    print name

root = Tk()
root.title("Network Attack Detector")

# create a menu
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=openfiledialog)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=callback)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=callback)

# create a canvas
canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()

y = int(CANVAS_HEIGHT / 2)
canvas.create_line(0,y,CANVAS_WIDTH, y, fill="#476042")

fig = plt.figure()

mainloop()
