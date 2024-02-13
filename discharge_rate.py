import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import csv
import pandas as pd

# read file line by line, and do some cleaning,
# if it sees a line that starts with time:
# it will append the time to the time list
# the same line will have bottom force:
# append force to the force list
# time: 2.40307, RTF: 8237.53, bottom force: -5621.65

# filename = "dirty_output.txt"
time_list = []

fps = 2000
step_size = 1/fps

density = 2.5
radius = 0.02

bottom_y = -26 # bottom y coordinate, only look at particles below this y

folder_directory = "C:/Users/fang/Documents/pHX/cluster_data/orifice_x_0.9_mupw_0.50/data/"

start_frame = 2000
end_frame = 2099
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
with open(folder_directory + 'mass_flow_rate.pkl', 'wb') as f:
    pickle.dump([time_list, mass_from_particles], f)


plt.plot(time_list, mass_from_particles)
plt.xlabel("time")
plt.ylabel("mass (g) - from particles")
plt.show()





