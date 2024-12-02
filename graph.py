from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class RealTimeGraph:
    def __init__(self, master, equation):
        self.master = master
        self.equation = equation
        self.amplitude = 1
        self.frequency = 1

        # Matplotlib figure with transparent background
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="#2e2e2e")
        self.ax = self.fig.add_subplot(111, facecolor="#2e2e2e")
        
        # Plot with white line
        self.line, = self.ax.plot([], [], color='white')
        
        # Set axes limits
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-20, 20)
        
        # Customize axis appearance
        self.ax.spines['top'].set_color('white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.tick_params(colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        
        # Attach the canvas to Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Data
        self.x_data = np.linspace(0, 10, 1000)
        self.y_data = np.zeros(1000)

        self.update_plot()

    def update_plot(self):

        # this is where the equation is 
        self.y_data = self.equation(self.x_data, self.amplitude, self.frequency)
        self.line.set_data(self.x_data, self.y_data)
        self.canvas.draw()

        self.master.after(100, self.update_plot)