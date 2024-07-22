import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')

plt.close('all')

# Load the CSV files
pyblksim_data = pd.read_csv('./performance_results_pyblksim.csv')
simulink_data = pd.read_csv('./performance_results_simulink.csv')


# Function to plot Average and Peak Memory Usage vs Sampling Frequency
def plot_avg_peak_memory_usage_vs_sampling(data1, data2):
    avg_memory1 = data1.groupby('Sampling Frequency (Hz)')['Average Memory Usage (MiB)'].mean()
    avg_memory2 = data2.groupby('Sampling Frequency (Hz)')['Average Memory Usage (MiB)'].mean()
    peak_memory1 = data1.groupby('Sampling Frequency (Hz)')['Peak Memory Usage (MiB)'].max()
    peak_memory2 = data2.groupby('Sampling Frequency (Hz)')['Peak Memory Usage (MiB)'].max()
    
    plt.figure(figsize=(14, 8))
    
    # Plot Average Memory Usage
    plt.plot(avg_memory1.index, avg_memory1.values, label='pyblksim Average Memory Usage', marker='o')
    plt.plot(avg_memory2.index, avg_memory2.values, label='simulink Average Memory Usage', marker='x')
    
    # Plot Peak Memory Usage
    plt.plot(peak_memory1.index, peak_memory1.values, label='pyblksim Peak Memory Usage', marker='o', linestyle='--')
    plt.plot(peak_memory2.index, peak_memory2.values, label='simulink Peak Memory Usage', marker='x', linestyle='--')
    
    plt.xlabel('Sampling Frequency (Hz)')
    plt.ylabel('Memory Usage (MiB)')
    plt.title('Average and Peak Memory Usage vs Sampling Frequency')
    plt.legend(title='Memory Usage Type')
    plt.grid(True)
    plt.show()

# Plot Average and Peak Memory Usage vs Sampling Frequency for both scripts
plot_avg_peak_memory_usage_vs_sampling(pyblksim_data, simulink_data)
