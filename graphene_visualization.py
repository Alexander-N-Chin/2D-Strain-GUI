import tkinter as tk
from tkinter import ttk
from graphene import Graphene

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


def redraw_canvas(g: Graphene, canvas: tk.Canvas):
    # Clear the canvas
    canvas.delete("all")

    # Redraw the elements
    g.calculate_coords()
    g.draw_bonds(canvas)
    g.draw_atoms(canvas)


def update_canvas(g: Graphene, scale_dict: dict[str, tk.Scale], canvas):
    # Read the current values from the scales
    length_a = scale_dict["basis length(a)"].get()
    origin_x = scale_dict["origin x"].get()
    origin_y = scale_dict["origin y"].get()
    width = scale_dict["width"].get()
    length = scale_dict["length"].get()

    # Update the Graphene object
    g.a_length = length_a
    g.origin = (origin_x, g.origin[1]) if origin_x is not None else g.origin
    g.origin = (g.origin[0], origin_y) if origin_y is not None else g.origin
    g.width = width
    g.length = length
    
    # Redraw the canvas
    redraw_canvas(g, canvas)


def main():
    g = Graphene()

    # Create the main application window
    root = tk.Tk()
    root.title("Dark Theme Tkinter GUI")
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
        ("basis length(a)", 1, 100, 50),  # Adjust min and max as needed
        ("origin x", 0, 500, 80),
        ("origin y", 0, 500, 250),
        ("width", 1, 50, 7),
        ("length", 1, 50, 7)
    ]

    for label_text, min_val, max_val, default_val in input_fields:
        label = ttk.Label(left_frame, text=label_text)
        label.pack(pady=(20, 5), padx=5, anchor="w")
        scale = tk.Scale(left_frame, from_=min_val, to=max_val, orient="horizontal",
                         command=lambda _: update_canvas(g, scale_dict, canvas))
        scale.set(default_val)
        scale.pack(padx=5, fill="x")
        scale_dict[label_text] = scale

    # Create the right column for the canvas
    canvas_frame = ttk.Frame(main_frame)
    canvas_frame.pack(side="right", fill="both", expand=True)

    # Add a canvas to the right column
    canvas = tk.Canvas(canvas_frame, background="#1e1e1e")
    canvas.pack(fill="both", expand=True)

    # Initial canvas drawing
    redraw_canvas(g, canvas)
    
    root.mainloop()

if __name__ == "__main__":
    main()
