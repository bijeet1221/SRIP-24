import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')

plt.close('all')

# Load the CSV files
pyblksim_data = pd.read_csv('./performance_results_pyblksim.csv')
simulink_data = pd.read_csv('./performance_results_simulink.csv')


# Define the sampling frequencies to be plotted
sampling_frequencies = [1000, 32373, 184201, 2499999]

# Function to plot Execution Time vs Iteration for specified sampling frequencies in a 2x2 grid with legends inside the graphs
def plot_execution_time_vs_iteration_grid_internal_legend(data1, data2, frequencies):
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    axes = axes.flatten()
    
    for i, freq in enumerate(frequencies):
        subset1 = data1[data1['Sampling Frequency (Hz)'] == freq]
        subset2 = data2[data2['Sampling Frequency (Hz)'] == freq]
        
        axes[i].plot(subset1['Iteration'], subset1['Execution Time (s)'], label=f'pyblksim {freq} Hz')
        axes[i].plot(subset2['Iteration'], subset2['Execution Time (s)'], label=f'simulink {freq} Hz')
        
        axes[i].set_xlabel('Iteration')
        axes[i].set_ylabel('Execution Time (s)')
        axes[i].set_title(f'Execution Time vs Iteration at {freq} Hz')
        #axes[i].legend(title='Script and Sampling Frequency', loc='best')
        axes[i].grid(True)
    
    plt.tight_layout()
    plt.show()

# Plot Execution Time vs Iteration for the specified sampling frequencies in a 2x2 grid with internal legends
plot_execution_time_vs_iteration_grid_internal_legend(pyblksim_data, simulink_data, sampling_frequencies)
