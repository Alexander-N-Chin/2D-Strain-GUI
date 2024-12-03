from tkinter import Tk, Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class graph3D:
    def __init__(self, master):
        self.master = master

        # Constants
        self.b = 1
        self.a = 0.246  # nm, lattice constant
        self.gamma = 2.7  # eV

        # Tkinter frame for Matplotlib
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)

        # Matplotlib figure with transparent background
        self.fig_3d = Figure(figsize=(4, 8), dpi=100, facecolor="#2e2e2e")
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d', facecolor="#2e2e2e")

        # Attach the canvas to Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_3d, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initialize k-space grid
        self.init_k_space()

        # Plot the initial bands
        self.plot_bands()

        # Bind mouse events for rotation
        self.canvas.get_tk_widget().bind("<ButtonPress-1>", self.on_click)
        self.canvas.get_tk_widget().bind("<B1-Motion>", self.on_drag)
        self.canvas.get_tk_widget().bind("<ButtonRelease-1>", self.on_release)

        # State variables for mouse drag
        self.is_dragging = False
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0

        # update
        self.update()

    def init_k_space(self):
        """Initialize the k-space grid and energy bands."""
        kx_range = np.linspace(-2 * np.pi / self.a, 2 * np.pi / self.a, 300)
        ky_range = np.linspace(-2 * np.pi / self.a, 2 * np.pi / self.a, 300)
        self.kx, self.ky = np.meshgrid(kx_range, ky_range)

    def compute_bands(self):
        """Compute the energy bands based on the current parameters."""
        # note b does nothing
        alpha = np.sqrt(
            1 + 4 * np.cos(np.sqrt(3) * self.b * self.a / 2 * self.kx) * np.cos(self.b * self.a / 2 * self.ky) + 4 * np.cos(self.b * self.a / 2 * self.ky) ** 2
        )
        E_plus = self.gamma * alpha
        E_minus = -self.gamma * alpha
        return E_plus, E_minus

    def plot_bands(self):
        """Plot the conduction and valence bands."""
        self.ax_3d.clear()

        # Compute energy bands
        E_plus, E_minus = self.compute_bands()

        # Plot the conduction and valence bands
        self.ax_3d.plot_surface(self.kx, self.ky, E_plus, cmap='viridis', alpha=0.8, edgecolor='none')
        self.ax_3d.plot_surface(self.kx, self.ky, E_minus, cmap='plasma', alpha=0.8, edgecolor='none')

        # Axes labels
        self.ax_3d.set_xlabel('$k_x$ ($\mathrm{nm}^{-1}$)', color='white')
        self.ax_3d.set_ylabel('$k_y$ ($\mathrm{nm}^{-1}$)', color='white')
        self.ax_3d.set_zlabel('Energy $E(k)$ (eV)', color='white')
        # self.ax_3d.set_title('Graphene Band Structure (3D)', color='white')

        # Customize appearance
        self.ax_3d.tick_params(colors='white')
        self.ax_3d.xaxis.label.set_color('white')
        self.ax_3d.yaxis.label.set_color('white')
        self.ax_3d.zaxis.label.set_color('white')

    def on_click(self, event):
        """Handle mouse click to start rotation."""
        self.is_dragging = True
        self.prev_mouse_x = event.x
        self.prev_mouse_y = event.y

    def on_drag(self, event):
        """Handle mouse drag to update plot view."""
        if self.is_dragging:
            dx = event.x - self.prev_mouse_x
            dy = event.y - self.prev_mouse_y

            # Update azimuthal and elevation angles based on mouse movement
            self.ax_3d.view_init(elev=self.ax_3d.elev + dy * 0.1, azim=self.ax_3d.azim - dx * 0.1)

            # Redraw the canvas
            self.canvas.draw()

            # Update previous mouse position
            self.prev_mouse_x = event.x
            self.prev_mouse_y = event.y

    def on_release(self, event):
        """Handle mouse release to stop rotation."""
        self.is_dragging = False

    def update(self):
            self.compute_bands()
            self.plot_bands()
            self.canvas.draw()

            # Schedule the next update
            self.master.after(1000, self.update)  # Update every 100 ms

class graph2D:
    def __init__(self, master):
        self.master = master

        # Constants
        self.b = 1 # random variable
        self.a = 0.246  # nm, lattice constant
        self.gamma = 2.7  # eV

        # Tkinter frame for Matplotlib
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)

        # Matplotlib figure with transparent background
        self.fig_2d = Figure(figsize=(4, 4), dpi=100, facecolor="#2e2e2e")
        self.ax_2d = self.fig_2d.add_subplot(111, facecolor="#2e2e2e")

        # Attach the canvas to Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_2d, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initialize k-space grid
        self.init_k_space()

        # Plot the initial bands
        self.plot_bands()

        # get the latest new hits!
        self.update()

    def init_k_space(self):
        """Initialize the k-space grid and energy bands."""
        kx_range = np.linspace(-2 * np.pi / self.a, 2 * np.pi / self.a, 300)
        ky_range = np.linspace(-2 * np.pi / self.a, 2 * np.pi / self.a, 300)
        self.kx, self.ky = np.meshgrid(kx_range, ky_range)

    def compute_bands(self):
        """Compute the energy bands based on the current parameters."""
        # note b does nothing
        alpha = np.sqrt(
            1 + 4 * np.cos(np.sqrt(3) * self.b * self.a / 2 * self.kx) * np.cos(self.b * self.a / 2 * self.ky) + 4 * np.cos(self.b * self.a / 2 * self.ky) ** 2
        )
        E_plus = self.gamma * alpha
        E_minus = -self.gamma * alpha
        return E_plus, E_minus

    def plot_bands(self):
        """Plot the conduction and valence bands."""
        self.ax_2d.clear()

        # Compute energy bands
        E_plus, _ = self.compute_bands()

        # Plot contours for the conduction band
        contour_plus = self.ax_2d.contourf(self.kx, self.ky, E_plus, levels=100, cmap='viridis')
        
        # Add a continuous colorbar
        # cbar = self.fig_2d.colorbar(contour_plus, ax=self.ax_2d)
        # cbar.set_label("Conduction Band Energy (eV)", color='white')  # Set color of the label to white
        # cbar.ax.tick_params(labelcolor='white')  # Set color of colorbar ticks to white

        # Axes labels
        self.ax_2d.set_xlabel('$k_x$ ($\mathrm{nm}^{-1}$)', color='white')
        self.ax_2d.set_ylabel('$k_y$ ($\mathrm{nm}^{-1}$)', color='white')
        # self.ax_2d.set_title('Graphene Conduction Band (2D Contour)', color='white')

        # Customize appearance
        self.ax_2d.tick_params(colors='white')
        self.ax_2d.xaxis.label.set_color('white')
        self.ax_2d.yaxis.label.set_color('white')

    def update(self):
        self.compute_bands()
        self.plot_bands()
        self.canvas.draw()

        # Schedule the next update
        self.master.after(1000, self.update)  # Update every 1000 ms