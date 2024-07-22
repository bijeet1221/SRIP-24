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
sampling_frequencies = [1000, 77222, 2499999]

# Function to plot Execution Time vs Iteration for specified sampling frequencies
def plot_execution_time_vs_iteration(data1, data2, frequencies):
    plt.figure(figsize=(14, 8))
    
    for freq in frequencies:
        subset1 = data1[data1['Sampling Frequency (Hz)'] == freq]
        subset2 = data2[data2['Sampling Frequency (Hz)'] == freq]
        
        plt.plot(subset1['Iteration'], subset1['Execution Time (s)'], label=f'pyblksim {freq:.0e} Hz', marker='.')
        plt.plot(subset2['Iteration'], subset2['Execution Time (s)'], label=f'simulink {freq:.0e} Hz', marker='x')
    
    plt.xlabel('Iteration')
    plt.ylabel('Execution Time (s)')
    plt.title('Execution Time vs Iteration for Different Sampling Frequencies')
    plt.legend(title='Script and Sampling Frequency')
    plt.grid(True)
    plt.show()

# Plot Execution Time vs Iteration for the specified sampling frequencies for both scripts
plot_execution_time_vs_iteration(pyblksim_data, simulink_data, sampling_frequencies)
