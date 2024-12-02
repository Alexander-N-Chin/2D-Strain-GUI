import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class RealTimeGraph:
    def __init__(self, master):
        self.master = master
        master.title("Real-Time Graph")

        ## Input fields
        self.amplitude_label = tk.Label(master, text="Amplitude:")
        self.amplitude_label.pack()
        self.amplitude_entry = tk.Entry(master)
        self.amplitude_entry.insert(0, "1")
        self.amplitude_entry.pack()

        self.frequency_label = tk.Label(master, text="Frequency:")
        self.frequency_label.pack()
        self.frequency_entry = tk.Entry(master)
        self.frequency_entry.insert(0, "1")
        self.frequency_entry.pack()

        ## Matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([], [])
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-2, 2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.x_data = np.linspace(0, 10, 100)
        self.y_data = np.zeros(100)

        self.update_plot()

    def update_plot(self):
        # this is where you load the constants
        try:
            amplitude = float(self.amplitude_entry.get())
            frequency = float(self.frequency_entry.get())
        except ValueError:
            amplitude = 1
            frequency = 1

        # this is where the equation is 
        self.y_data = amplitude * np.sin(frequency * self.x_data)
        self.line.set_data(self.x_data, self.y_data)
        self.canvas.draw()

        self.master.after(100, self.update_plot)