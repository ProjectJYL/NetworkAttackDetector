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

style.use('ggplot')
LARGE_FONT = ("Verdana", 12)
        
lines = []
current_index = 0;
filename = ""

fig = Figure(figsize=(15,5), dpi=100)
afig = fig.add_subplot(111)
afig.set_xlabel("xdata")
afig.set_ylabel("ydata")
afig.set_adjustable('datalim')
afig.plot([],[],'r',[],[],'g')
afig.xaxis.set_animated(True)
afig.set_ylim(-1,1)
fig.legend(afig.get_lines(),("line 1","line 2"),"upper right")

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
    for i in xdata:
        afig.annotate(s="(%s,%s)"%(xdata[i],y1data[i]),
                      xy=(xdata[i],y1data[i]),
                      xycoords="data")
        afig.annotate(s="(%s,%s)"%(xdata[i],y2data[i]),
                      xy=(xdata[i],y2data[i]),
                      xycoords="data")

    current_index = current_index + 1;
    return afig.lines
        
def openfilecb():
    global filename, current_index, xdata,y1data, y2data
    
    filename = tk.filedialog.askopenfilename()
    current_index = 0
    xdata,y1data, y2data = [],[], []      
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

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

            
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
##        labelvar = tk.StringVar()
##        xylabel = tk.Label(self, textvariable=labelvar)
##        xylabel.pack()
##        labelvar.set("x,y")
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.mpl_connect("pick_event", onpick)
        


app = SeaofBTCapp()
ani = animation.FuncAnimation(fig, update,blit=True,
                              interval=10)
app.mainloop()

        

        
