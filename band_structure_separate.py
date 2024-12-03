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

# Create a 3D plot for the band structure
fig_3d = plt.figure(figsize=(12, 8))
ax_3d = fig_3d.add_subplot(111, projection='3d')

# Plot the conduction and valence bands
ax_3d.plot_surface(kx, ky, E_plus, cmap='viridis', alpha=0.8, edgecolor='none', label="Conduction Band")
ax_3d.plot_surface(kx, ky, E_minus, cmap='plasma', alpha=0.8, edgecolor='none', label="Valence Band")

# Axes labels
ax_3d.set_xlabel('$k_x$ ($\mathrm{nm}^{-1}$)')
ax_3d.set_ylabel('$k_y$ ($\mathrm{nm}^{-1}$)')
ax_3d.set_zlabel('Energy $E(k)$ (eV)')
ax_3d.set_title('Graphene Band Structure (3D)')

# Show 3D plot
plt.tight_layout()
plt.show()

# Create a 2D contour plot for the conduction band
fig_2d, ax_2d = plt.subplots(figsize=(10, 8))

# Plot contours for the conduction band
contour_plus = ax_2d.contourf(kx, ky, E_plus, levels=100, cmap='viridis')

# Add a continuous colorbar
cbar = fig_2d.colorbar(contour_plus, ax=ax_2d)
cbar.set_label("Conduction Band Energy (eV)")

# Axes labels and title
ax_2d.set_xlabel('$k_x$ ($\mathrm{nm}^{-1}$)')
ax_2d.set_ylabel('$k_y$ ($\mathrm{nm}^{-1}$)')
ax_2d.set_title('Graphene Conduction Band (2D Contour)')

# Show 2D plot
plt.tight_layout()
plt.show()