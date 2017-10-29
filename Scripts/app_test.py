import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

# make the plot live
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')

LARGE_FONT = ("Verdana", 12)

class SeaofBTCapp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #change the style of our window a bit 
        # tk.Tk.iconbitmap('/home/jialee/Pictures/python-logo.gif')
        tk.Tk.wm_title(self, "Network Attack Detector")
        #create the first main frame
        container = tk.Frame(self)
        container.pack(side="top",fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # make the graph frame
        frame = GraphPage(container, self)
        self.frames[GraphPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(GraphPage)
        frame.a.clear()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def animate(i):
##        pullData = open('sample.txt','r').read()
##        dataArray = pullData.split('\n')
##        xar = []
##        yar = []
##        for eachline in dataArray:
##            if len(eachline) > 1:
##                x,y = eachline.split(',')
##                xar.append(int(x))
##                yar.append(int(y))
        frame.a.clear()
            
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                           command = lambda: qf("Check it out, i'm passing vars"))
        button.pack()

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Homepage", command=
                             lambda: controller.showframe(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
                           
def qf(quickPrint):
    print(quickPrint)
    
##class PageThree(tk.Frame):
##    def __init__(self,parent,controller):
##        tk.Frame.__init__(self,parent)
##        label = tk.Label(self, text ="Graph Page!", font=LARGE_FONT)
##        label.pack(pady=10,padx=10)
##
##        button1 = ttk.Button(self, text="Back to Home",
##                             command=lambda: controller.show_frame(StartPage))
##        button1.pack()

app = SeaofBTCapp()
app.mainloop()

        

        
