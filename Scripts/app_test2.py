import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.lines import Line2D
import numpy as np
import random

style.use('ggplot')
LARGE_FONT = ("Verdana", 12)
        
#parameters
current_index = 0
current_index2 = 0
filename = ""
INTERVAL = 10
plot = False
mcavData = []
xlen = 1000


#live graph
fig = Figure(figsize=(15,5), dpi=100)
afig = fig.add_subplot(111)
afig.set_xlabel("xdata")
afig.set_ylabel("ydata")
afig.set_adjustable('datalim')
afig.plot([],[],'r',[],[],'g')
afig.set_ylim(-1,1)
afig.set_xbound(0,10)
fig.legend(afig.get_lines(),("y1","y2"),"upper right")

#mcav data
fig2 = Figure(figsize=(15,5), dpi=100)
afig2 = fig2.add_subplot(111)
afig2.set_xlabel("xdata")
afig2.set_ylabel("ydata")
afig2.set_adjustable('datalim')
afig2.plot([],[],'b')
afig2.set_ylim(0,1)
afig2.set_xbound(0,10)

def line_picker(line, mouseevent):
        """
        find the points within a certain distance from the mouseclick in
        data coords and attach some extra attributes, pickx and picky
        which are the data points that were picked
        """
        if mouseevent.xdata is None:
            return False, dict()
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        maxd = 0.05
        d = np.sqrt((xdata - mouseevent.xdata)**2. + (ydata - mouseevent.ydata)**2.)

        ind = np.nonzero(np.less_equal(d, maxd))
        if len(ind):
            pickx = np.take(xdata, ind)
            picky = np.take(ydata, ind)
            props = dict(ind=ind, pickx=pickx, picky=picky)
            return True, props
        else:
            return False, dict()

def onpick(event):
    print('(%s,%s)' % (str(event.pickx), str(event.picky)))
    return
    
def update(frame):
    global current_index
    global filename

    if(len(filename) < 1):
        return afig.lines

    data = open(filename,'r').read()    
    dataline = data.split('\n')
    if(current_index > len(dataline) ):
        return afig.lines
    
    xdata, y1data, y2data = [],[],[]        
    for eachline in dataline[:current_index]:
        if(len(eachline)>1):
            x,y1,y2 = eachline.split(',')
            xdata.append(int(x))
            y1data.append(float(y1))
            y2data.append(float(y2))           

    afig.clear()
    afig.plot(xdata,y1data,'r',
        xdata,y2data,'g',picker=line_picker)
    # annotation isn't quite right
##    for i in xdata:
##        afig.annotate(s="(%s,%s)"%(xdata[i],y1data[i]),
##                      xy=(xdata[i],y1data[i]),
##                      xycoords="data")
##        afig.annotate(s="(%s,%s)"%(xdata[i],y2data[i]),
##                      xy=(xdata[i],y2data[i]),
##                      xycoords="data")

    current_index = current_index + 1;
    return afig.lines

def update2(frame):
        global current_index2,plot,mcavData
        
        if(not plot):
                return afig2.lines
        
        xdata = np.arange(0,1000)
        for i in xdata:
                y = random.randrange(0,1001)/1000.00
                mcavData.append(y)
                
        afig2.clear()
        afig2.plot(xdata[:current_index2],mcavData[:current_index2],'b')
        current_index2 = current_index2 + 1
        return afig2.lines
        
def openfilecb():
    global filename, current_index
    
    filename = tk.filedialog.askopenfilename()
    current_index = 0
    return

def callback():
    filename = tk.filedialog.askopenfilename()
    return

def aboutappcb():
    title = "About"
    message="Network Attack Detector. Version 1.0"
    tk.filedialog.messagebox.showinfo(title,message)
    return

def quitappcb():
    global app
    if(tk.filedialog.messagebox.askokcancel("Warning",
                                            "Do you really want to quit?")):
        print("Quit")
        app.destroy()
        app.quit()
        
    else:
        print("Quit canceled")
    return

def setplotcb():
        global plot,mcavData,current_index2
        plot = not plot

        if(plot):
                current_index2 = 0
                afig2.clear()
                mcavData = []
    
class SeaofBTCapp(tk.Tk):        
    def __init__(self):
        tk.Tk.__init__(self)
        var_text = tk.StringVar()
        #change the style of our window a bit 
        # tk.Tk.iconbitmap('/home/jialee/Pictures/python-logo.gif')
        tk.Tk.wm_title(self, "Network Attack Detector")
        #create notebook tab
        tab = ttk.Notebook(self)
        tab.pack()
        #create the first main frame
        container = tk.Frame(self)
        container.pack(side="top",fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        #create the second main frame
        container2 = tk.Frame(self)
        container2.pack(side="top",fill="both", expand=True)
        container2.grid_rowconfigure(0, weight=1)
        container2.grid_columnconfigure(0, weight=1)
        # add tab
        tab.add(container, text="y data plot")
        tab.add(container2, text="MCAV")
        # make the menu frame
        menu = tk.Menu(self)
        self.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...",command= openfilecb)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quitappcb)
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Help",  menu=helpmenu)
        helpmenu.add_command(label="About", command=aboutappcb)
        # make the graph frame
        frame = GraphPage(container, self)
        self.frames[GraphPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(GraphPage)
        # make the mcav frame
        frame = MCAV_Page(container2, self)
        self.frames[MCAV_Page] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MCAV_Page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

            
class MCAV_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = FigureCanvasTkAgg(fig2,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        #Add a plot button to start plotting
        start = ttk.Button(self, text="Plot", command=setplotcb)
        start.pack()

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.mpl_connect("pick_event", onpick)
        


app = SeaofBTCapp()
ani = animation.FuncAnimation(fig,update,blit=True,interval=INTERVAL)
ani2 = animation.FuncAnimation(fig2,update2,blit=True,interval=INTERVAL)
app.mainloop()

        
