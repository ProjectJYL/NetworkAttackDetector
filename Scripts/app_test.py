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

##f = Figure(figsize=(5,5), dpi=100)
##a = f.add_subplot(111)
fig, ax = plt.subplots(figsize=(15,5))
xdata, y1data, y2data = [],[],[]
ln1, ln2= plt.plot([], [], [], [], animated=True)

def init():
##    ax.set_xlim(0, 1000)
    ax.set_ylim(-2, 2)
    ax.set_xlabel("xdata")
    ax.set_ylabel("ydata")
    ln1.set_label("line1")
    ln2.set_label("line2")
    ax.set_xbound(0,1000)
    plt.legend()
    return ln1,ln2

def update(frame):
    global lines
    global current_index

    if(len(lines) < 1):
        print('Err:file data is not read into the array.')
        return ln1, ln2

    if(current_index >= len(lines)):
        print('EOF is reached. No new data to be plotted.')
        return ln1, ln2
        
    x,y1,y2 = lines[current_index].split(',')
    xdata.append(int(x))
    y1data.append(float(y1))
    y2data.append(float(y2))
    ln1.set_data(xdata,y1data)
    ln2.set_data(xdata,y2data)
##    upperx = 100+int(x)
##    lowerx = int(x)-1
##    ax.set_xlim(left=lowerx,right=upperx)
    current_index = current_index + 1;
    return ln1, ln2

        
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
        plt.clf()
        fig.clear()
        ax.set_xlim(0,100,auto=True)
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

##        button1 = ttk.Button(self, text="Back to Homepage", command=
##                             lambda: controller.showframe(StartPage))
##        button1.pack()

##        f = Figure(figsize=(5,5), dpi=100)
##        a = f.add_subplot(111)
##        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        canvas = FigureCanvasTkAgg(fig, self)
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
ani = animation.FuncAnimation(fig, update, frames=list(range(0,1000)),
                              interval=10)
##ani = animation.FuncAnimation(fig, update, init_func=init,
##                              blit=True, interval=1000)

app.mainloop()

        

        
