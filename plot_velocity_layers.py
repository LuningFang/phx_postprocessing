import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import csv


tube_radius = 0.2
horizontal_pitch = 1.2
vertical_pitch = 1
tube_spacing_x = horizontal_pitch - 2 * tube_radius
tube_spacing_y = vertical_pitch   - 2 * tube_radius



# Load pickled file named velocity_field.pickle
# pickle_file_name = "../cluster_data/oriface_x_0.4_mupw_0.50/velocity_field_400micron_wall_4cm.pickle"
pickle_file_name = "../cluster_data/9cm/velocity_field_400micron_wall_9cm.pickle"

with open(pickle_file_name, 'rb') as pickle_file:
    vx_2D, vy_2D, vz_2D, vel_mag_2D, x_range, y_range = pickle.load(pickle_file)

v_out = 1

vel_mag_2D = vel_mag_2D * 10 /v_out
vx_2D = vx_2D * 10/v_out
vy_2D = vy_2D * 10/v_out
vz_2D = vz_2D * 10/v_out

dim_x = 2 * tube_spacing_x     + 2*tube_radius
dim_y = tube_spacing_y * 3 + 4 * tube_radius


# dim_x = 5
# dim_y = 18
# dim_y = 1.5

center_x = 0
center_y = -10.5
# center_y = -7.8
num_colors = 50

# inlet_id = 100
# outlet_id = 10

# inlet_id = 5
# outlet_id = 0

# avg_inlet_velo  = np.mean(vel_mag_2D[inlet_id])        
# avg_outlet_velo = np.mean(vel_mag_2D[outlet_id])



# vel_mag_2D with the one computed from vx_2D and vy_2D
for i in range(len(x_range)):
    for j in range(len(y_range)):
        vel_mag_2D[j][i] = np.sqrt(vx_2D[j][i]**2 + vy_2D[j][i]**2)


max_vel_mag = np.max(vel_mag_2D)
# find the maximum velocity location
max_vel_mag_loc = np.where(vel_mag_2D == max_vel_mag)
max_vel_mag_loc_x = x_range[max_vel_mag_loc[1][0]]
max_vel_mag_loc_y = y_range[max_vel_mag_loc[0][0]]
print("max velo {:.2f}, located at {:.2f}, {:.2f}".format(max_vel_mag, max_vel_mag_loc_x, max_vel_mag_loc_y))

custom_cmap = plt.get_cmap('coolwarm', num_colors)
# max_vel_mag = 2.5
norm = mcolors.Normalize(vmin=0, vmax=max_vel_mag)

# Plot the velocity field
fig, ax = plt.subplots(figsize=(dim_x * 5, dim_y*3))

# Make a quiver plot of the velocity field
# The color of the arrows represents the magnitude of the velocity

# I don't want scaling of the arrow, all arrow same length 
quiver = ax.quiver(x_range, y_range, vx_2D, vy_2D, vel_mag_2D, cmap=custom_cmap, norm=norm, scale=400, width=0.005)
# quiver = ax.quiver(x_range, y_range, vx_2D, vy_2D, vel_mag_2D, cmap=custom_cmap, scale=1000, width=0.005)

# Add colorbar
cbar = plt.colorbar(quiver, ax=ax, ticks=np.linspace(0, max_vel_mag, 20))
cbar.set_label(r'normalized velocity magnitude u/u$_{ref}$', rotation=90, labelpad=10)  

# Set plot limits
plt.xlim([-dim_x/2 + center_x, dim_x/2 + center_x])
plt.ylim([-dim_y/2 + center_y, dim_y/2 + center_y])
plt.gca().set_aspect('equal')

# Set labels
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')


# Add circles
# read circle position from blender_videos/cylinder_pos.txt
# header is x,y,z

# read csv file cylinder_pos.csv, header is "x,y,z"
offset_y = 0
cylinder_radius = 0.2

with open("blender_videos/cylinder_pos.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for row in reader:
        circle_pos_x = float(row[0])
        circle_pos_y = float(row[1]) + offset_y
        # plot circle with transparent filling 



        circle = plt.Circle((circle_pos_x, circle_pos_y), cylinder_radius, color='blue', alpha=0.8, fill=True)
        plt.gca().add_artist(circle)


# add title
# title = "$v_{{in}}={:.2f} mm/s$, $v_{{out}}={:.2f}$ mm/s".format(avg_inlet_velo, avg_outlet_velo)


# plt.title(title)

plt.savefig("9cm.png",dpi=500,bbox_inches='tight')
plt.show()