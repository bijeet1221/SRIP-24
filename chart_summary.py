import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')

plt.close('all')


# Load the CSV files
pyblksim_df = pd.read_csv('./performance_results_pyblksim.csv')
simulink_df = pd.read_csv('./performance_results_simulink.csv')


# Calculate average and peak execution time and memory usage grouped by sampling frequency
pyblksim_summary = pyblksim_df.groupby('Sampling Frequency (Hz)').agg({
    'Execution Time (s)': ['mean', 'max'],
    'Peak Memory Usage (MiB)': ['mean', 'max'],
    'Average Memory Usage (MiB)': ['mean', 'max']
}).reset_index()

simulink_summary = simulink_df.groupby('Sampling Frequency (Hz)').agg({
    'Execution Time (s)': ['mean', 'max'],
    'Peak Memory Usage (MiB)': ['mean', 'max'],
    'Average Memory Usage (MiB)': ['mean', 'max']
}).reset_index()

# Prepare for iteration plots for three different sampling frequencies
sampling_frequencies = [1000, 2499999]

fig, axes = plt.subplots(1, 4, figsize=(15, 7))

# Plot 1: Execution Time (Average & Peak) vs Sampling Frequency
axes[0].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Execution Time (s)', 'mean')], label='pyblksim Avg', marker='x')
axes[0].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Execution Time (s)', 'max')], label='pyblksim Peak', marker='x')
axes[0].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Execution Time (s)', 'mean')], label='simulink Avg', marker='.')
axes[0].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Execution Time (s)', 'max')], label='simulink Peak', marker='.')
axes[0].set_title('Execution Time vs Sampling Frequency')
axes[0].set_xlabel('Sampling Frequency (Hz)')
axes[0].set_ylabel('Time (s)')
axes[0].legend()

# Plot 2: Execution Time vs Iterations for three different sampling frequencies
for freq in sampling_frequencies:
    pyblksim_subset = pyblksim_df[pyblksim_df['Sampling Frequency (Hz)'] == freq]
    simulink_subset = simulink_df[simulink_df['Sampling Frequency (Hz)'] == freq]
    axes[1].plot(pyblksim_subset['Iteration'], pyblksim_subset['Execution Time (s)'], label=f'pyblksim {freq:.0e}', marker='x')
    axes[1].plot(simulink_subset['Iteration'], simulink_subset['Execution Time (s)'], label=f'simulink {freq:.0e}', marker='.')

axes[1].set_title('Execution Time vs Iterations')
axes[1].set_xlabel('Iteration')
axes[1].set_ylabel('Time (s)')
axes[1].legend()

# Plot 3: Memory Usage (Average & Peak) vs Sampling Frequency
axes[2].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Average Memory Usage (MiB)', 'mean')], label='pyblksim Avg', marker='x')
axes[2].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Average Memory Usage (MiB)', 'max')], label='pyblksim Peak', marker='x')
axes[2].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Average Memory Usage (MiB)', 'mean')], label='simulink Avg', marker='.')
axes[2].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Average Memory Usage (MiB)', 'max')], label='simulink Peak', marker='.')
axes[2].set_title('Memory Usage vs Sampling Frequency')
axes[2].set_xlabel('Sampling Frequency (Hz)')
axes[2].set_ylabel('Memory (MiB)')
axes[2].legend()

# Plot 4: Memory Usage vs Iterations for three different sampling frequencies
for freq in sampling_frequencies:
    pyblksim_subset = pyblksim_df[pyblksim_df['Sampling Frequency (Hz)'] == freq]
    simulink_subset = simulink_df[simulink_df['Sampling Frequency (Hz)'] == freq]
    axes[3].plot(pyblksim_subset['Iteration'], pyblksim_subset['Average Memory Usage (MiB)'], label=f'pyblksim {freq:.0e}', marker='x')
    axes[3].plot(simulink_subset['Iteration'], simulink_subset['Average Memory Usage (MiB)'], label=f'simulink {freq:.0e}', marker='.')

axes[3].set_title('Memory Usage vs Iterations')
axes[3].set_xlabel('Iteration')
axes[3].set_ylabel('Memory (MiB)')
axes[3].legend()

plt.tight_layout()
plt.show()
