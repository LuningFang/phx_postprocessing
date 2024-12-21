import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Set matplotlib parameters
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams.update({'font.size': 25})
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
MARKERSIZE = 5

# Parameters
# folders = ["../August/20PERCENT_Q_3e-3/", "../August/30PERCENT_Q_3e-3/", "../August/40PERCENT_Q_3e-3/"]
# folders = ["../August/20PERCENT_Q_3e-3/", "../August/parallal_plates/Test2_Q_3e-3/"]
# folders = ["../August/20PERCENT_Q_3e-3/", "../August/10PERCENT_Q_2e-3/"]
# folders = [ "../Teardrop/40PERCENT_Q_3e-3/"]

folders = ["../August/5times_ks_sameQ/50PERCENT_nopins/"]
# folders = ["../August/parallel_plates/Test4/"]
# folders = ["../TO_design/results_temp/"]
# output_csv_name = "test.csv"
output_csv_name = "5times_ks_same_Q_bulk_velo_avg_temperature_Test5_nopins.csv"

labels = ["pins, 50% valve"]
# start_frame = 170
# end_frame = start_frame + 30  # For testing
start_frame = 70
end_frame = 101
y_min = -20.5
# y_max = -3
y_max = -3
binsize_y = 0.05  # note ths bin is 0.05 for other cases!!!
particle_density = 3.6

def process_data(folder_name, start_frame, end_frame, y_min, y_max, binsize_y, particle_density):
    # Create arrays to store the data
    Y_array = np.arange(y_max, y_min, -binsize_y)
    temp_avg_array = np.zeros(len(Y_array))
    total_mass = np.zeros(len(Y_array))

    # Process each frame
    for frame in range(start_frame, end_frame):
        filename = folder_name + "DEM_frame_{:05d}.csv".format(frame)
        data = pd.read_csv(filename, header=0)
        print("Loaded data from", filename)

        # Extract the data
        x = data['X']
        y = data['Y']
        z = data['Z']
        temp = data['Temp']
        r = data['r']
        vy = data['v_y']

        # now set every element in vy to be 1, not just vy = 1
        # vy[:] = 1
        

        # Compute mass and temp*mass arrays
        mass = 4/3 * np.pi * r**3 * particle_density
        temp_mass = temp * mass * np.abs(vy)
        # temp_mass = temp * mass

        # Accumulate data for each bin
        for i in range(len(Y_array)):
            roi_indices = np.where((y < Y_array[i] + binsize_y) & (y > Y_array[i]))[0]
            temp_avg_array[i] += np.sum(temp_mass.iloc[roi_indices])
            total_mass[i] += np.sum(mass.iloc[roi_indices] * np.abs(vy.iloc[roi_indices]))
            # total_mass[i] += np.sum(mass.iloc[roi_indices])

    # Compute the average temperature
    temp_avg_array = np.divide(temp_avg_array, total_mass, out=np.zeros_like(temp_avg_array), where=total_mass!=0)

    return Y_array, temp_avg_array

# Plotting
plt.figure()

# colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# how do i use default python colors?
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

for folder in folders:
    Y_array, temp_avg_array = process_data(folder, start_frame, end_frame, y_min, y_max, binsize_y, particle_density)
    plt.plot(Y_array[0] - Y_array, temp_avg_array, label=labels[folders.index(folder)], color=colors[folders.index(folder)])


plt.xlabel("Y position (cm)")
# ylabel, temperature in C
plt.ylabel("Temperature (\N{DEGREE SIGN}C)")
plt.title("Averaged bulk temperature at the cross section")
plt.grid(which='both')
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
plt.xlim(Y_array[0] - Y_array[0], Y_array[0] - Y_array[-1])
plt.legend()
plt.tight_layout()
plt.show()

# save Y_array and temp_avg_array to one csv file, separate by comma
# save the data to a csv file
data = np.array([Y_array[0] - Y_array, temp_avg_array])
data = data.T
np.savetxt(output_csv_name, data, delimiter=",", header="Y_pos,Temp", comments="")