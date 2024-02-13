# pickle PIV results of the entire domain
# time average from 0.5 to 1.0 seconds
# 
import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('Agg')  # Set the Agg backend
import csv as csv
import pandas as pd
import matplotlib.colors as mcolors
# Y up

# use cgs units
tube_radius = 0.2
horizontal_pitch = 1.2
vertical_pitch = 1
tube_spacing_x = horizontal_pitch - 2 * tube_radius
tube_spacing_y = vertical_pitch   - 2 * tube_radius

# particle_diameter = 0.025
particle_diameter = 0.04

# read data
folder_name = "../cluster_data/orifice_x_0.9_mupw_0.50/data/"


# define region of plot interest
dim_x = 5
dim_y = 14
center_x = 0
center_y = -12.6

dim_z = 0.5
print("dim_x: {}".format(dim_x))
print("dim_y: {}".format(dim_y))

# center_x = 0
# center_y = -10.5


numBins = 40
test_section_xdim = dim_x
bin_size_x = test_section_xdim / numBins
bin_size_y = bin_size_x
bin_size_z = particle_diameter


# draw a contour plot of velocity magnitude
# first, convert the data into a 2D array
# define the x and y range
x_range = np.arange(-dim_x/2 + center_x + bin_size_x*0.5, dim_x/2 + center_x, bin_size_x)
y_range = np.arange(-dim_y/2 + center_y + bin_size_y*0.5, dim_y/2 + center_y, bin_size_y)

# contour plot size
print("contour plot size: {} by {}".format(len(x_range), len(y_range)))


# loop through all time steps from 0 to 100
# for pic_step in range(0, avg_end):

# create a 2D array
vel_mag_2D = np.zeros((len(y_range),len(x_range)))

# create 2D array vx, vy and vz
vx_2D = np.zeros((len(y_range),len(x_range)))
vy_2D = np.zeros((len(y_range),len(x_range)))
vz_2D = np.zeros((len(y_range),len(x_range)))


# create a counter for computing the number of particles in each bin
counter = np.zeros((len(y_range),len(x_range)))

step_size = 1/2000
start_frame =  1001
end_frame = 1250

for kk in range(start_frame, end_frame): 

    # compute the time step
    file_name = folder_name  + "discharge_{:06d}.csv".format(kk)
    print("reading file {}".format(file_name)) 
    # read csv file
    data = pd.read_csv(file_name,header=0)

    # extract x,y,z,vx,vy,vz columns
    x = data['x']
    y = data['y']
    z = data['z']
    vx = data['vx']
    vy = data['vy']
    vz = data['vz']

    print("time: {:.4f}".format(kk * step_size))

    # go through all particles, find particles where x and y are within the region of interest
    # and store their velocities and positions
    vel_x = []
    vel_y = []
    vel_z = []
    pos_x = []
    pos_y = []
    pos_z = []
    vel_mag = []


    for i in range(len(x)):
        if (x[i] > -dim_x/2 + center_x and x[i] < dim_x/2 + center_x and y[i] > -dim_y/2 + center_y and y[i] < dim_y/2 + center_y):
            if (z[i] > dim_z/2 - 2 * particle_diameter):
            # if (np.abs(z[i]) < particle_diameter):
            
                vel_x.append(vx[i])
                vel_y.append(vy[i])
                vel_z.append(vz[i])
                # vel_mag.append(np.sqrt(vx[i]**2 + vy[i]**2 + vz[i]**2))
                vel_mag.append(np.sqrt(vx[i]**2 + vy[i]**2))

                pos_x.append(x[i])
                pos_y.append(y[i])
                pos_z.append(z[i])


    # go through all particles, find the bin that it belongs to, and add its velocity to the bin
    for i in range(len(pos_x)):
        # find the bin that the particle belongs to
        x_bin = int((pos_x[i] - (-dim_x/2 + center_x))/bin_size_x)
        y_bin = int((pos_y[i] - (-dim_y/2 + center_y))/bin_size_y)
        # add the velocity to the bin
        vel_mag_2D[y_bin][x_bin] = vel_mag_2D[y_bin][x_bin] + vel_mag[i]
        vx_2D[y_bin][x_bin] = vx_2D[y_bin][x_bin] + vel_x[i]
        vy_2D[y_bin][x_bin] = vy_2D[y_bin][x_bin] + vel_y[i]
        vz_2D[y_bin][x_bin] = vz_2D[y_bin][x_bin] + vel_z[i]


        # increment the counter
        counter[y_bin][x_bin] = counter[y_bin][x_bin] + 1

# compute the average velocity in each bin
for i in range(len(y_range)):
    for j in range(len(x_range)):
        # do not 
        # if counter[i][j] <= 2 and counter[i][j] > 0:
        #     print("bin ID: {}, {}, pos {}, {},  counters: {}, vel_mag {}".format(i, j, pos_x[i], pos_y[j], counter[i][j], vel_mag_2D[i][j] / counter[i][j]))

        #     vx_2D[i][j] = 0
        #     vy_2D[i][j] = 0
        #     vz_2D[i][j] = 0
        #     vel_mag_2D[i][j] = 0


        if counter[i][j] != 0:
            vel_mag_2D[i][j] = vel_mag_2D[i][j] / counter[i][j]
            vx_2D[i][j] = vx_2D[i][j] / counter[i][j]
            vy_2D[i][j] = vy_2D[i][j] / counter[i][j]
            vz_2D[i][j] = vz_2D[i][j] / counter[i][j]

# save vx_2D, vy_2D, vz_2D, vel_mag_2D, x_range, y_range to a pickle file
pickle_file_name = "velocity_field_400micron_wall_4cm_entire.pickle"
pickle_file = open(folder_name + pickle_file_name, 'wb')
pickle.dump([vx_2D, vy_2D, vz_2D, vel_mag_2D, x_range, y_range], pickle_file)
pickle_file.close()
