import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Setup matplotlib parameters
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams.update({'font.size': 20})
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)

# Constants
z_type = "wall"
shape = "cylinder"
tube_radius = 0.2  # Actual radius of the pins
inflate_radius = 0.05  # Additional inflation for masking

# List of pin positions
cylinder_px_list = [-1.2, 0, 1.2, -0.6, 0.6, -1.2, 0, 1.2, -0.6, 0.6, -1.2, 0, 1.2]
cylinder_py_list = [-12.5, -12.5, -12.5, -13.5, -13.5, -14.5, -14.5, -14.5, -15.5, -15.5, -16.5, -16.5, -16.5]

# Load pickled data
folder_name = "../Oct/20PERCENT_Q_3e-3/"
pickle_file_name = folder_name + "center_piv.pickle"

with open(pickle_file_name, 'rb') as pickle_file:
    vx_2D, vy_2D, vz_2D, vel_mag_2D, x_range, y_range = pickle.load(pickle_file)

# Calculate grid spacing (assuming uniform grid for simplicity)
dx = x_range[1] - x_range[0]
dy = y_range[1] - y_range[0]

# Initialize strain rate array
strain_rate_2D = np.zeros((len(y_range), len(x_range)))
shear_strain_2D = np.zeros((len(y_range), len(x_range)))

# Function to check if a point is inside any pin
def is_inside_pin(x, y, px_list, py_list, radius):
    for (pin_x, pin_y) in zip(px_list, py_list):
        distance_to_pin = np.sqrt((x - pin_x)**2 + (y - pin_y)**2)
        if distance_to_pin < radius:
            return True
    return False

# Loop through each grid point to calculate the velocity gradients and strain rate
for i in range(1, len(y_range) - 1):
    for j in range(1, len(x_range) - 1):
        # Check if the current point or its neighbors are inside a pin
        if is_inside_pin(x_range[j], y_range[i], cylinder_px_list, cylinder_py_list, tube_radius) or \
           is_inside_pin(x_range[j+1], y_range[i], cylinder_px_list, cylinder_py_list, tube_radius) or \
           is_inside_pin(x_range[j-1], y_range[i], cylinder_px_list, cylinder_py_list, tube_radius) or \
           is_inside_pin(x_range[j], y_range[i+1], cylinder_px_list, cylinder_py_list, tube_radius) or \
           is_inside_pin(x_range[j], y_range[i-1], cylinder_px_list, cylinder_py_list, tube_radius):
            # If the point or its neighbors are inside a pin, skip the calculation
            strain_rate_2D[i, j] = 0
            shear_strain_2D[i, j] = 0
        else:
            # Compute finite differences for velocity gradients
            dvx_dx = (vx_2D[i,   j+1] - vx_2D[i,   j-1]) / (2 * dx)
            dvy_dy = (vy_2D[i+1, j] - vy_2D[i-1, j]) / (2 * dy)
            
            dvx_dy = (vx_2D[i+1, j] - vx_2D[i-1, j]) / (2 * dy)
            dvy_dx = (vy_2D[i, j+1] - vy_2D[i, j-1]) / (2 * dx)
            

            # Strain rate tensor (symmetric part of the velocity gradient tensor)
            epsilon_xx = dvx_dx
            epsilon_yy = dvy_dy
            epsilon_xy = 0.5 * (dvx_dy + dvy_dx)  # Shear strain

            # Strain rate magnitude (simplified scalar measure of strain rate)
            strain_rate_2D[i, j] = np.sqrt(epsilon_xx**2 + epsilon_yy**2 + 2 * epsilon_xy**2)
            shear_strain_2D[i, j] = np.sqrt(epsilon_xy**2)

# Create subplots: 1 row, 2 columns (side-by-side)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Assuming 'shear_strain_2D' and 'strain_rate_2D' are your strain data arrays
# Plot the shear strain on the left (first subplot)
c1 = axes[0].contourf(x_range, y_range, shear_strain_2D, levels=100)
fig.colorbar(c1, ax=axes[0], label=r'$|\dot{\epsilon}_{xy}|$')  # Shear strain rate colorbar
axes[0].set_title('Shear Strain Rate')
axes[0].set_xlabel('X (cm)')
axes[0].set_ylabel('Y (cm)')
axes[0].set_aspect('equal')  # Make axes equal for circles


# Plot the total strain on the right (second subplot)
c2 = axes[1].contourf(x_range, y_range, strain_rate_2D, levels=100)
fig.colorbar(c2, ax=axes[1], label=r'$\dot{\gamma} = \sqrt{\dot{\epsilon}_{xx}^2 + \dot{\epsilon}_{yy}^2 + 2\dot{\epsilon}_{xy}^2}$')  # Total strain rate colorbar
axes[1].set_title('Total Strain Rate')
axes[1].set_xlabel('X (cm)')
axes[1].set_aspect('equal')  # Make axes equal for circles

# Add the mask for pins on both subplots
for ax in axes:
    for ii in range(len(cylinder_px_list)):
        circle = plt.Circle((cylinder_px_list[ii], cylinder_py_list[ii]), tube_radius, color='white', fill=True)
        ax.add_artist(circle)

# Extract '20PERCENT' from folder_name for the title
parsed_title = folder_name.split('/')[-2].split('_')[0]  # Extract from folder name
fig.suptitle(f"Strain Rate Comparison ({parsed_title})")

plt.tight_layout()
plt.show()