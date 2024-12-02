import tkinter as tk
from tkinter import ttk, ALL
from graphene import Graphene
from graph import RealTimeGraph
import numpy as np

# Define the dark theme colors
def set_dark_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame", background="#2e2e2e")
    style.configure("TButton", background="#444", foreground="white", relief="flat")
    style.map(
        "TButton",
        background=[("active", "#555")],
        foreground=[("active", "#fff")],
    )
    style.configure("TLabel", background="#2e2e2e", foreground="white")


def redraw_canvas_lattice(g: Graphene, canvas: tk.Canvas):
    # Clear the canvas
    canvas.delete("all")

    # Redraw the elements
    g.calculate_coords()
    g.draw_bonds(canvas)
    g.draw_atoms(canvas)

def redraw_canvas_recip(g: Graphene, canvas: tk.Canvas):
    # Clear the canvas
    canvas.delete("all")

    # Redraw the elements
    g.calc_reciprocal_lattice()
    g.draw_reciprocal_bonds(canvas)
    g.draw_reciprocal_atoms(canvas)


def update_canvas(g: Graphene, r1: RealTimeGraph, r2: RealTimeGraph, scale_dict: dict[str, tk.Scale], lattice_canvas, recip_canvas):
    # Read the current values from the scales
    width = scale_dict["width"].get()
    length = scale_dict["length"].get()

    # Update the Graphene object
    g.width = width
    g.length = length
    r1.amplitude = width
    r1.frequency = length
    r2.amplitude = width
    r2.frequency = length
    
    # Redraw the canvas
    redraw_canvas_lattice(g, lattice_canvas)
    redraw_canvas_recip(g, recip_canvas)


def do_zoom(event, canvas):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    factor = 1.001 ** event.delta
    canvas.scale(ALL, x, y, factor, factor)


def main():
    g = Graphene()

    # Create the main application window
    root = tk.Tk()
    root.title("Graphene Strain GUI")
    root.geometry("800x600")

    set_dark_theme(root)

    # Create a main frame to hold everything
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Create a left column for sliders
    left_frame = ttk.Frame(main_frame, height=500)
    left_frame.pack(side="left", fill="y")

    # Create a dictionary to store the scales
    scale_dict = {}

    # Create a list of labels and input sliders (Scale widgets)
    input_fields = [
        ("width", 1, 20, 15),
        ("length", 1, 20, 15)
    ]

    for label_text, min_val, max_val, default_val in input_fields:
        label = ttk.Label(left_frame, text=label_text)
        label.pack(pady=(20, 5), padx=5, anchor="w")
        scale = tk.Scale(left_frame, from_=min_val, to=max_val, orient="horizontal",
                         command=lambda _: update_canvas(g, r1, r2, scale_dict, lattice_canvas, recip_canvas))
        scale.set(default_val)
        scale.pack(padx=5, fill="x")
        scale_dict[label_text] = scale

    # Create the right column for the canvas
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(side="right", fill="both", expand=True)

    # create sin graph
    def sinwave(x:float, amp:float, freq:float):
        y = amp * np.sin(x * freq) 
        return y
    r1 = RealTimeGraph(graph_frame, sinwave)

    # create log graph
    def logwave(x:float, amp:float, freq:float):
        y = amp * np.log10(x * freq) 
        return y
    r2 = RealTimeGraph(graph_frame, logwave)

    # Create the brave lattice column for the canvas
    canvas_frame = ttk.Frame(main_frame, width=500)
    canvas_frame.pack(side="right", fill="both", expand=True)

    # Add a canvas to the right column
    lattice_canvas = tk.Canvas(canvas_frame, background="#1e1e1e", width = 1000)
    lattice_canvas.bind("<MouseWheel>", lambda event: do_zoom(event, lattice_canvas)) # WINDOWS ONLY
    lattice_canvas.bind('<ButtonPress-1>', lambda event: lattice_canvas.scan_mark(event.x, event.y))
    lattice_canvas.bind("<B1-Motion>", lambda event: lattice_canvas.scan_dragto(event.x, event.y, gain=1))
    lattice_canvas.pack(fill="both", expand=True)

    # Add a canvas to the reciprocal column
    recip_canvas = tk.Canvas(canvas_frame, background="#1e1e1e", width=1000)
    recip_canvas.bind("<MouseWheel>", lambda event: do_zoom(event, recip_canvas)) # WINDOWS ONLY
    recip_canvas.bind('<ButtonPress-1>', lambda event: recip_canvas.scan_mark(event.x, event.y))
    recip_canvas.bind("<B1-Motion>", lambda event: recip_canvas.scan_dragto(event.x, event.y, gain=1))
    recip_canvas.pack(fill="both", expand=True)

    # Initial canvas drawing
    redraw_canvas_recip(g, recip_canvas)
    redraw_canvas_lattice(g, lattice_canvas)

    root.mainloop()

if __name__ == "__main__":
    main()
