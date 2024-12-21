import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib

import matplotlib.pyplot as plt


# Set global matplotlib parameters
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams.update({'font.size': 25})
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
MARKERSIZE = 20
# Inputs
distance = 179.4  # Total distance in mm
position_array = np.array([0, 17.94, 35.88, 53.82, 71.76, 89.7, 107.64, 125.58, 143.52, 161.46, distance])  # Positions in mm


def compute_conductance_dem(inlet_temp, input_heat, measured_surface_temp, outlet_temp):
    # Calculate slope and intercept for bulk temperature
    slope = (outlet_temp - inlet_temp) / distance
    intercept = inlet_temp

    # Calculate bulk temperature at each interior position (skipping the first and last positions)
    bulk_temp = slope * position_array[1:-1] + intercept

    # Calculate interpolated surface temperature (if required)
    surface_slope, surface_intercept = np.polyfit(position_array[1:-1], measured_surface_temp, 1)

    surface_slope = 0
    surface_intercept = 80
    # Calculate interpolated surface temperature
    measured_surface_temp = surface_slope * position_array[1:-1] + surface_intercept

    # Calculate delta T at each position
    delta_T = measured_surface_temp - bulk_temp

    # Compute conductance at each position
    conductance = input_heat / delta_T

    # Calculate average conductance
    average_conductance = np.mean(conductance)
    return average_conductance


def process_file(filename):
    data = pd.read_csv(filename)
    num_tests = data.shape[0]
    conductance_array = np.zeros(num_tests)

    # Loop through each test
    for i in range(num_tests):
        # Extract data
        inlet_temp = data["inletTemp"][i]
        outlet_temp = data["outletTemp"][i]
        specific_heat = data["specific_heat"][i]
        specific_heat = 733
        flow_rate = data["flowrate"][i]
        input_heat = specific_heat * flow_rate * (outlet_temp - inlet_temp)

        # Measured surface temperatures
        measured_surface_temp = data.loc[i, [
            "SurfaceTemp1", "SurfaceTemp2", "SurfaceTemp3", "SurfaceTemp4",
            "SurfaceTemp5", "SurfaceTemp6", "SurfaceTemp7", "SurfaceTemp8", "SurfaceTemp9"
        ]].values

        # Calculate conductance
        conductance = compute_conductance_dem(inlet_temp, input_heat, measured_surface_temp, outlet_temp)
        conductance_array[i] = conductance

        # print flow rate vs outlet temperature 
        print(f"Flow Rate: {flow_rate * 1e3:.6f} g/sec, Outlet temp: {outlet_temp:.2f} °C")


    return data["flowrate"].values, conductance_array


# Process the two datasets
# filename2 = "temp_results/Temp_matrix_teardrop_dem.csv"
# filename1 = "temp_results/Temp_matrix_cyl_dem.csv"

filename1 = "temp_results/Temp_matrix_5times_ks_nopins_dem.csv"
filename2 = "temp_results/Temp_matrix_5times_ks_same_Q_nopins_dem.csv"
# filename2 = "temp_results/Temp_matrix_const_cyl_dem.csv"

print("cylindrical pins")
flowrate1, conductance_array1 = process_file(filename1)
# print("\nCylindrical Pins")
flowrate2, conductance_array2 = process_file(filename2)
# flowrate3, conductance_array3 = process_file(filename2)


# Plot the results
plt.figure(figsize=(8, 6))
plt.plot(flowrate1 * 1e3, conductance_array1, 'o-', label='Cylindrical Pins')
plt.plot(flowrate2 * 1e3, conductance_array2, 'd-', label='Teardrop Pins') 
# plt.plot(flowrate3 * 1e3, conductance_array3, 's-', label='10 times larger')

plt.xlabel('Flow Rate (g/sec)')
plt.ylabel('Conductance (W/K)')
plt.title('DEM Conductance vs Flow Rate, Constant Heat Flux Boundary')
# add both major and minor grid lines 
plt.grid(which='both')
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')


plt.legend()
plt.grid()

plt.show()
