import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt

style.use('ggplot')
LARGE_FONT = ("Verdana", 12)
        
lines = []
current_index = 1;

fig = Figure(figsize=(15,5), dpi=100)
a = fig.add_subplot(111)
a.plot([],[],[],[])
fig.legend(a.get_lines(),("line 1","line 2"),"upper right")

def init():
    a.set_ylim(-2,2)
    a.set_xlim(0,1000)
    a.set_xlabel("xdata")
    a.set_ylabel("ydata")
    return a.lines

def update(frame):
    global current_index
    global lines

    if(len(lines)<1):
        return a.lines
    
    xdata, y1data, y2data = [],[],[]        
    for eachline in lines[:current_index]:
        if(len(eachline)>1):
            x,y1,y2 = eachline.split(',')
            xdata.append(int(x))
            y1data.append(float(y1))
            y2data.append(float(y2))
    
    a.plot(xdata,y1data,'r', label= 'line1')
    a.plot(xdata,y2data,'g', label= 'line2')
    current_index = current_index + 1;
    return a.lines
        
def openfilecb():
    global lines
    global current_index
    global xdata,y1data, y2data
    
    filename = tk.filedialog.askopenfilename()
    fo = open(filename,'r')
    lines = []
    lines = fo.readlines();
    fo.close()
    if(fo.closed):
        current_index = 1
        xdata,y1data, y2data = [],[], []
        print('File "%s" is opened and read successfully' %filename)
        
    return

def callback():
    filename = tk.filedialog.askopenfilename()
    print(filename)
    return

def aboutappcb():
    title = "About Network Attack Detector"
    message="Version 1.0                        "
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
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
                           
def qf(quickPrint):
    print(quickPrint)

app = SeaofBTCapp()
ani = animation.FuncAnimation(fig, update, init_func=init, blit = True,
                              interval=10)
app.mainloop()

        

        
