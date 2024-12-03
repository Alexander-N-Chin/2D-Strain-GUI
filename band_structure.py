import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
a = 0.246  # nm, lattice constant
gamma = 2.7  # eV

# Define k-space grid
kx_range = np.linspace(-2 * np.pi / a, 2 * np.pi / a, 300)
ky_range = np.linspace(-2 * np.pi / a, 2 * np.pi / a, 300)
kx, ky = np.meshgrid(kx_range, ky_range)

# Alpha formula
alpha = np.sqrt(
    1 + 4 * np.cos(np.sqrt(3) * a / 2 * kx) * np.cos(a / 2 * ky) + 4 * np.cos(a / 2 * ky) ** 2
)

# Energy bands
E_plus = gamma * alpha
E_minus = -gamma * alpha

# Create a 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the conduction and valence bands
ax.plot_surface(kx, ky, E_plus, cmap='viridis', alpha=0.8, edgecolor='none', label="Conduction Band")
ax.plot_surface(kx, ky, E_minus, cmap='plasma', alpha=0.8, edgecolor='none', label="Valence Band")

# Add contours
ax.contour(kx, ky, E_plus, zdir='z', offset=0, cmap='viridis', linestyles="solid")
ax.contour(kx, ky, E_minus, zdir='z', offset=0, cmap='plasma', linestyles="solid")

# Axes labels
ax.set_xlabel('$k_x$ ($\mathrm{nm}^{-1}$)')
ax.set_ylabel('$k_y$ ($\mathrm{nm}^{-1}$)')
ax.set_zlabel('Energy $E(k)$ (eV)')
ax.set_title('Graphene Band Structure')

# Show plot
plt.tight_layout()
plt.show()