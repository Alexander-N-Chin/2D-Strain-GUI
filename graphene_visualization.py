import tkinter as tk
from tkinter import ttk, ALL
from graphene import Graphene
from graph import graph3D, graph2D, graph1D

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


def update_canvas(g: Graphene, r1: graph3D, r2: graph2D, r3: graph1D, scale_dict: dict[str, tk.Scale], lattice_canvas):
    # Read the current values from the scales
    shear = scale_dict["shear strain"].get()
    zigzag = scale_dict["zigzag strain"].get()
    armchair = scale_dict["armchair strain"].get()

    # Update the Graphene object
    r1.gamma_s = r2.gamma_s = r3.gamma_s = g.gamma_s = shear
    r1.epsilon_z = r2.epsilon_z = r3.epsilon_z = g.epsilon_z = zigzag
    r1.epsilon_a = r2.epsilon_a = r3.epsilon_a = g.epsilon_a = armchair
    
    # Redraw the canvas
    redraw_canvas_lattice(g, lattice_canvas)


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
    root.geometry("1200x600")

    set_dark_theme(root)

    # Create a main frame to hold everything
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Create a left column for sliders
    left_frame = ttk.Frame(main_frame, height=500)
    left_frame.pack(side="left", fill="y")

    # Create a dictionary to store the scales
    scale_dict = {}

    # Define the list of input fields with parameters
    input_fields = [
        ("shear strain", -.2, .2, 0.0),
        ("zigzag strain", -.30, .30, 0.0),
        ("armchair strain", -.25, .25, 0.0)
    ]

    # Create input sliders and labels dynamically
    for label_text, min_val, max_val, default_val in input_fields:
        # Create and pack the label
        label = ttk.Label(left_frame, text=label_text)
        label.pack(pady=(20, 5), padx=5, anchor="w")  # Add spacing for aesthetics

        # Create the slider (Scale widget) with dynamic range, float resolution, and callback
        scale = tk.Scale(
            left_frame,
            from_=min_val,  # Minimum value of the slider
            to=max_val,     # Maximum value of the slider
            orient="horizontal",  # Slider orientation
            resolution=0.01,  # Set step size for floating-point increments
            command=lambda value, key=label_text: update_canvas(
                g, r1, r2, r3, scale_dict, lattice_canvas
            )  # Pass current slider values to the callback
        )
        scale.set(default_val)  # Set the default value of the slider
        scale.pack(padx=5, fill="x")  # Allow the slider to expand horizontally

        # Store the slider in the dictionary with the label text as the key
        scale_dict[label_text] = scale

    # Create the right column for the canvas
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(side="right", fill="both", expand=True)

    r2 = graph2D(graph_frame)
    r3 = graph1D(graph_frame)

    # Create the right column for the canvas
    graph_frame2 = ttk.Frame(main_frame)
    graph_frame2.pack(side="right", fill="both", expand=True)

    r1 = graph3D(graph_frame2)

    # Create the brave lattice column for the canvas
    canvas_frame = ttk.Frame(main_frame, width=500)
    canvas_frame.pack(fill="both", expand=True)

    # Add a canvas to the right column
    lattice_canvas = tk.Canvas(canvas_frame, background="#1e1e1e", width = 300)
    lattice_canvas.bind("<MouseWheel>", lambda event: do_zoom(event, lattice_canvas)) # WINDOWS ONLY
    lattice_canvas.bind('<ButtonPress-1>', lambda event: lattice_canvas.scan_mark(event.x, event.y))
    lattice_canvas.bind("<B1-Motion>", lambda event: lattice_canvas.scan_dragto(event.x, event.y, gain=1))
    lattice_canvas.pack(fill="both", expand=True)

    # # Add a canvas to the reciprocal column
    # recip_canvas = tk.Canvas(canvas_frame, background="#1e1e1e", width=300)
    # recip_canvas.bind("<MouseWheel>", lambda event: do_zoom(event, recip_canvas)) # WINDOWS ONLY
    # recip_canvas.bind('<ButtonPress-1>', lambda event: recip_canvas.scan_mark(event.x, event.y))
    # recip_canvas.bind("<B1-Motion>", lambda event: recip_canvas.scan_dragto(event.x, event.y, gain=1))
    # recip_canvas.pack(fill="both", expand=True)

    # Initial canvas drawing
    # redraw_canvas_recip(g, recip_canvas)
    redraw_canvas_lattice(g, lattice_canvas)

    root.mainloop()

if __name__ == "__main__":
    main()
