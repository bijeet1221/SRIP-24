import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')

plt.close('all')

# Load the CSV files
pyblksim_data = pd.read_csv('./performance_results_pyblksim.csv')
simulink_data = pd.read_csv('./performance_results_simulink.csv')

# Function to plot Average and Peak Execution Time vs Sampling Frequency
def plot_avg_peak_execution_time_vs_sampling(data1, data2):
    avg_runtime1 = data1.groupby('Sampling Frequency (Hz)')['Execution Time (s)'].mean()
    avg_runtime2 = data2.groupby('Sampling Frequency (Hz)')['Execution Time (s)'].mean()
    peak_runtime1 = data1.groupby('Sampling Frequency (Hz)')['Execution Time (s)'].max()
    peak_runtime2 = data2.groupby('Sampling Frequency (Hz)')['Execution Time (s)'].max()
    
    plt.figure(figsize=(14, 8))
    
    # Plot Average Execution Time
    plt.plot(avg_runtime1.index, avg_runtime1.values, label='pyblksim Average Execution Time', marker='o')
    plt.plot(avg_runtime2.index, avg_runtime2.values, label='simulink Average Execution Time', marker='x')
    
    # Plot Peak Execution Time
    plt.plot(peak_runtime1.index, peak_runtime1.values, label='pyblksim Peak Execution Time', marker='o', linestyle='--')
    plt.plot(peak_runtime2.index, peak_runtime2.values, label='simulink Peak Execution Time', marker='x', linestyle='--')
    
    plt.xlabel('Sampling Frequency (Hz)')
    plt.ylabel('Execution Time (s)')
    plt.title('Average and Peak Execution Time vs Sampling Frequency')
    plt.legend(title='Execution Time Type')
    plt.grid(True)
    plt.show()

# Plot Average and Peak Execution Time vs Sampling Frequency for both scripts
plot_avg_peak_execution_time_vs_sampling(pyblksim_data, simulink_data)
