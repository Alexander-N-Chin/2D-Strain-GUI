from tkinter import Tk, Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class graph3D:
    def __init__(self, master):
        self.master = master

        # Constants
        self.b = 1
        self.beta = 3                                        # some number 2-3
        self.a = 0.246                                          # nm, lattice constant
        self.delta = [self.a/2 * np.array([np.sqrt(3), 1]),     # hopping integral to nearest neighbors
                self.a/2 * np.array([-np.sqrt(3), 1]),          # hopping integral to nearest neighbors
                self.a * np.array([0, -1])]                     # hopping integral to nearest neighbors
        self.t_0 = 35                                            # assume for simplicity
        self.gamma_s = 0
        self.epsilon_a = 0
        self.epsilon_z = 0

        # Tkinter frame for Matplotlib
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)

        # Matplotlib figure with transparent background
        self.fig_3d = Figure(figsize=(6, 8), dpi=100, facecolor="#2e2e2e")
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
        kx_range = np.linspace(-15, 15, 500)
        ky_range = np.linspace(-15, 15, 500)
        self.kx, self.ky = np.meshgrid(kx_range, ky_range)

    def compute_bands(self):
        """Compute the energy bands based on the current parameters."""
        # Hamiltonian terms
        epsilon = np.array([[self.epsilon_z, self.gamma_s], [self.gamma_s, self.epsilon_a]])
        t = [
            self.t_0 * np.exp(-self.beta * np.linalg.norm((np.dot((np.eye(2) + epsilon), delta))) / self.a)
            for delta in self.delta
        ]
        
        gamma = sum(ti ** 2 for ti in t)
        g = np.zeros_like(self.kx)

        # Compute the g term, including the epsilon contribution
        for n in range(len(self.delta)):
            for s in range(n + 1, len(self.delta)):
                delta_diff = self.delta[n] - self.delta[s]
                # Include epsilon in the phase term
                phase = np.dot(
                    np.dot(np.stack((self.kx, self.ky), axis=0).T, np.eye(2) + epsilon), 
                    delta_diff
                )
                g += 2 * t[n] * t[s] * np.cos(phase)


        # Energy bands
        E_plus = np.sqrt(gamma + g)
        E_minus = -np.sqrt(gamma + g)

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
        self.beta = 2.7                                         # some number 2-3
        self.a = 0.246                                          # nm, lattice constant
        self.delta = [self.a/2 * np.array([np.sqrt(3), 1]),     # hopping integral to nearest neighbors
                self.a/2 * np.array([-np.sqrt(3), 1]),          # hopping integral to nearest neighbors
                self.a * np.array([0, -1])]                     # hopping integral to nearest neighbors
        self.t_0 = 1                                            # assume for simplicity
        self.gamma_s = 0
        self.epsilon_a = 0
        self.epsilon_z = 0

        # Tkinter frame for Matplotlib
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)

        # Matplotlib figure with transparent background
        self.fig_2d = Figure(figsize=(3, 3), dpi=100, facecolor="#2e2e2e")
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
        kx_range = np.linspace(-15, 15, 100)
        ky_range = np.linspace(-15, 15, 100)
        self.kx, self.ky = np.meshgrid(kx_range, ky_range)


    def compute_bands(self):
        """Compute the energy bands based on the current parameters."""
        # Hamiltonian terms
        epsilon = np.array([[self.epsilon_z, self.gamma_s], [self.gamma_s, self.epsilon_a]])
        t = [
            self.t_0 * np.exp(-self.beta * np.linalg.norm((np.dot((np.eye(2) + epsilon), delta))) / self.a)
            for delta in self.delta
        ]
        
        gamma = sum(ti ** 2 for ti in t)
        g = np.zeros_like(self.kx)

        # Compute the g term, including the epsilon contribution
        for n in range(len(self.delta)):
            for s in range(n + 1, len(self.delta)):
                delta_diff = self.delta[n] - self.delta[s]
                # Include epsilon in the phase term
                phase = np.dot(
                    np.dot(np.stack((self.ky, self.kx), axis=0).T, np.eye(2) + epsilon), 
                    delta_diff
                )
                g += 2 * t[n] * t[s] * np.cos(phase)


        # Energy bands
        E_plus = np.sqrt(gamma + g)
        E_minus = -np.sqrt(gamma + g)

        return E_plus, E_minus


    def plot_bands(self):
        """Plot the conduction and valence bands."""
        self.ax_2d.clear()

        # Compute energy bands
        E_plus, _ = self.compute_bands()

        # Plot filled contours for the conduction band
        contour_plus_filled = self.ax_2d.contourf(self.kx, self.ky, E_plus, levels=20, cmap='viridis')

        # Plot line contours for the conduction band
        contour_plus_lines = self.ax_2d.contour(self.kx, self.ky, E_plus, levels=20, colors='grey', linewidths=0.5)

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
        self.master.after(100, self.update)  # Update every 1000 ms


class graph1D:
    def __init__(self, master):
        self.master = master

        # Constants
        self.beta = 2.7  # Some number between 2-3
        self.a = 0.246  # nm, lattice constant
        self.delta = [self.a/2 * np.array([np.sqrt(3), 1]),  # Hopping integral to nearest neighbors
                      self.a/2 * np.array([-np.sqrt(3), 1]),  # Hopping integral to nearest neighbors
                      self.a * np.array([0, -1])]  # Hopping integral to next-nearest neighbors
        self.t_0 = 35  # Assume for simplicity
        self.gamma_s = 0
        self.epsilon_a = 0
        self.epsilon_z = 0

        # Tkinter frame for Matplotlib
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)

        # Matplotlib figure with transparent background
        self.fig_2d = Figure(figsize=(3, 6), dpi=100, facecolor="#2e2e2e")
        self.ax_2d = self.fig_2d.add_subplot(111, facecolor="#2e2e2e")

        # Attach the canvas to Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_2d, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initialize k-space path
        self.init_k_path()

        # Plot the initial bands
        self.plot_bands()

        # Get the latest new hits!
        self.update()

    def init_k_path(self):
        """Initialize the k-space path for M to Gamma to K to M."""
        # Define the high-symmetry points in the Brillouin zone (in units of 1/a)
        M1 = np.array([0, 8])
        Gamma = np.array([0, 0])
        K = np.array([10, 0])
        M2 = np.array([0, 8])

        # Define the path: M -> Gamma -> K -> M
        self.k_path = [M1, Gamma, K, M2]
        self.k_points = np.linspace(M1, Gamma, 1000).tolist() + np.linspace(Gamma, K, 1000).tolist() + np.linspace(K, M2, 1000).tolist()

        # Convert the k-points to numpy array for computations
        self.k_points = np.array(self.k_points)


    def compute_bands(self):
        """Compute the energy bands based on the current parameters."""
        # Hamiltonian terms
        epsilon = np.array([[self.epsilon_z, self.gamma_s], [self.gamma_s, self.epsilon_a]])
        t = [
            self.t_0 * np.exp(-self.beta * np.linalg.norm((np.eye(2) + epsilon).dot(delta)) / self.a)
            for delta in self.delta
        ]

        gamma = sum(ti ** 2 for ti in t)
        g = np.zeros(len(self.k_points))

        # Compute the g term, including the epsilon contribution
        for n in range(len(self.delta)):
            for s in range(n + 1, len(self.delta)):
                delta_diff = self.delta[n] - self.delta[s]
                # Include epsilon in the phase term
                phase = np.dot(
                    np.dot(self.k_points, np.eye(2) + epsilon),
                    delta_diff
                )
                g += 2 * t[n] * t[s] * np.cos(phase)

        # Energy bands
        E_plus = np.sqrt(gamma + g)
        E_minus = -np.sqrt(gamma + g)

        return E_plus, E_minus


    def plot_bands(self):
        """Plot the conduction and valence bands."""
        self.ax_2d.clear()

        # Compute energy bands
        E_plus, _ = self.compute_bands()

        # Plot band structure along the k-path
        self.ax_2d.plot(range(len(self.k_points)), E_plus, label='Conduction Band', color='aqua')
        self.ax_2d.plot(range(len(self.k_points)), -E_plus, label='Valence Band', color='red')

        # Mark high-symmetry points (M, Γ, K)
        k_labels = ['M', 'Γ', 'K', 'M']
        k_indices = [0, 999, 1999, 2999]  # Adjust these indices if needed
        for i, label in zip(k_indices, k_labels):
            self.ax_2d.annotate(label, (i, E_plus[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='white')

        # Set custom x-ticks at the indices of the high-symmetry points
        self.ax_2d.set_xticks(k_indices)
        self.ax_2d.set_xticklabels(k_labels, color='white')

        # Set white outlines for the axes
        for spine in self.ax_2d.spines.values():
            spine.set_color('white')
            spine.set_linewidth(1)

        # Customize tick parameters for white color
        self.ax_2d.tick_params(colors='white')

        # Customize grid lines to be white
        self.ax_2d.grid(color='white', linestyle='--')

        # Axes labels and title
        self.ax_2d.set_xlabel('k-point', color='white')
        self.ax_2d.set_ylabel('Energy (eV)', color='white')
        self.ax_2d.set_title('Band Structure: M -> Γ -> K -> M', color='white')


    def update(self):
        self.compute_bands()
        self.plot_bands()
        self.canvas.draw()

        # Schedule the next update
        self.master.after(100, self.update)  # Update every 1000 ms
