import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import csv
import pandas as pd
import platform
import sys
import os
import re


orifice_x_dim = 0.7
# check if cluster is used
useCluster = platform.system() != 'Windows'

# if there is command line input, then use that as the orifice diameter
if len(sys.argv) > 1:
    orifice_x_dim = float(sys.argv[1])

time_list = []

fps = 2000
step_size = 1/fps

density = 2.5
radius = 0.02

bottom_y = -26 # bottom y coordinate, only look at particles below this y

if useCluster:
    # use orifice size as the folder directory
    folder_directory = "/srv/home/fang/phX/CLUSTER_DATA/400um/orifice_x_{:.1f}_mupw_0.50/".format(orifice_x_dim)
else:
    # use orifice size as the folder directory
    folder_directory = "C:/Users/fang/Documents/pHX/cluster_data/orifice_x_{:.1f}_mupw_0.50/data/".format(orifice_x_dim)

# find the number of files in the folder_directory, they start with discharge, and format is csv
folder_files = os.listdir(folder_directory)
# get all files that start with discharge and end with .csv
folder_files = [f for f in folder_files if re.match(r'discharge_\d+.csv', f)]
# get the number of files
num_files = len(folder_files)


if useCluster:
    start_frame = 200
    end_frame = num_files
else:
    start_frame = 2000
    end_frame = start_frame + num_files -1


mass_from_particles = []
print("start frame: {} end frame: {}".format(start_frame, end_frame))
for i in range(start_frame, end_frame):
    filename = folder_directory + "discharge_{:06d}.csv".format(i)
    counter = 0
    # processing ...
    print("processing file: {}".format(filename))
    # read file with pd.read_csv
    df = pd.read_csv(filename, header=0)
    # get the velocity column
    velocity = df['absv']
    py = df['y']

    # num of particles is the length of of velocity
    n_particles = len(velocity)

    # look at particles where y is less than -24.5
    # and velocity is less than 0.1
    for pi in range(0, n_particles):
        if py[pi] < bottom_y and velocity[pi] < 0.1:
            counter += 1
    
    # append the force to the force list
    volume = 4/3 * np.pi * radius**3
    mass = counter * volume * density
    mass_from_particles.append(mass)

    time_list.append(i * step_size)

# plot mass vs time
# match size of time list with mass list, spacing is 0.01 sec
time_list = np.array(time_list)
# time_list = np.arange(0, len(mass_from_particles) * 0.01, 0.01)


# pickle time_list and mass_from_particles together for future use
# pick time and mass from particles into a pickle file 
import pickle

# make new directory called pickles
import os
if not os.path.exists(folder_directory + 'pickles'):
    os.makedirs(folder_directory + 'pickles')
pickle_directory = folder_directory + 'pickles/'

with open(pickle_directory + 'mass_flow_rate.pkl', 'wb') as f:
    pickle.dump([time_list, mass_from_particles], f)

# if not use cluster then plot
if not useCluster:
    plt.plot(time_list, mass_from_particles)
    plt.xlabel('Time (s)')
    plt.ylabel('Mass flow rate (kg/s)')
    plt.title('Mass flow rate vs time')
    plt.show()
