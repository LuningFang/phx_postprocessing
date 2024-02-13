import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import csv
import pandas as pd


time_list = []

useCluster = False

# check operating system, if windows, useCluster is set to false, else true
import platform
if platform.system() == 'Windows':
    useCluster = False
else:
    useCluster = True



fps = 2000
step_size = 1/fps

density = 2.5
radius = 0.02

bottom_y = -26 # bottom y coordinate, only look at particles below this y

if useCluster:
    folder_directory = "/srv/home/fang/phX/CLUSTER_DATA/400um/orifice_x_0.9_mupw_0.50/"
else:
    folder_directory = "C:/Users/fang/Documents/pHX/cluster_data/orifice_x_0.9_mupw_0.50/data/"

# adjust frame rate
start_frame = 200
end_frame = 2999


num_files = end_frame - start_frame + 1
mass_from_particles = []

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
