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
sampling_frequencies = [1000, 2499999]

# Function to plot Average and Peak Memory Usage vs Iteration for specified sampling frequencies in a single graph
def plot_avg_peak_memory_usage_vs_iteration_single_graph(data1, data2, frequencies):
    plt.figure(figsize=(14, 8))
    
    for freq in frequencies:
        subset1 = data1[data1['Sampling Frequency (Hz)'] == freq]
        subset2 = data2[data2['Sampling Frequency (Hz)'] == freq]
        
        avg_memory1 = subset1.groupby('Iteration')['Average Memory Usage (MiB)'].mean()
        avg_memory2 = subset2.groupby('Iteration')['Average Memory Usage (MiB)'].mean()
        peak_memory1 = subset1.groupby('Iteration')['Peak Memory Usage (MiB)'].max()
        peak_memory2 = subset2.groupby('Iteration')['Peak Memory Usage (MiB)'].max()
        
        plt.plot(avg_memory1.index, avg_memory1.values, label=f'pyblksim {freq} Hz Average Memory Usage', marker='o')
        plt.plot(avg_memory2.index, avg_memory2.values, label=f'simulink {freq} Hz Average Memory Usage', marker='x')
        
        plt.plot(peak_memory1.index, peak_memory1.values, label=f'pyblksim {freq} Hz Peak Memory Usage', marker='o', linestyle='--')
        plt.plot(peak_memory2.index, peak_memory2.values, label=f'simulink {freq} Hz Peak Memory Usage', marker='x', linestyle='--')
    
    plt.xlabel('Iteration')
    plt.ylabel('Memory Usage (MiB)')
    plt.title('Average and Peak Memory Usage vs Iteration for Different Sampling Frequencies')
    plt.legend(title='Memory Usage Type')
    plt.grid(True)
    plt.show()

# Plot Average and Peak Memory Usage vs Iteration for the specified sampling frequencies in a single graph
plot_avg_peak_memory_usage_vs_iteration_single_graph(pyblksim_data, simulink_data, sampling_frequencies)
