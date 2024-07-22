import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')

plt.close('all')


# Load the CSV files
pyblksim_df = pd.read_csv('./performance_results_pyblksim.csv')
simulink_df = pd.read_csv('./performance_results_simulink.csv')

bdsim_df = pd.read_csv('./performance_results_bdsim.csv')

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

bdsim_summary = bdsim_df.groupby('Sampling Frequency (Hz)').agg({
    'Execution Time (s)': ['mean', 'max'],
    'Average Memory Usage (MiB)': ['mean', 'max']
}).reset_index()

# Prepare for iteration plots for three different sampling frequencies
sampling_frequencies = [1000, 2499999]

fig, axes = plt.subplots(1, 4, figsize=(15, 7))

# Plot 1: Execution Time (Average & Peak) vs Sampling Frequency
axes[0].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Execution Time (s)', 'mean')], label='pyblksim, Avg', marker='x')
axes[0].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Execution Time (s)', 'max')], label='pyblksim, Peak', marker='x')
axes[0].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Execution Time (s)', 'mean')], label='simulink, Avg', marker='.')
axes[0].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Execution Time (s)', 'max')], label='simulink, Peak', marker='.')
axes[0].set_title('a.')
axes[0].set_xlabel('$F_S$: Sampling Frequency (Hz)')
axes[0].set_ylabel('Execution Time (s)')
axes[0].legend()

# Plot 2: Execution Time vs Iterations for three different sampling frequencies
for freq in sampling_frequencies:
    pyblksim_subset = pyblksim_df[pyblksim_df['Sampling Frequency (Hz)'] == freq]
    simulink_subset = simulink_df[simulink_df['Sampling Frequency (Hz)'] == freq]
    axes[1].plot(pyblksim_subset['Iteration'], pyblksim_subset['Execution Time (s)'], label=f'pyblksim, $F_S$: {freq:.0e}', marker='x')
    axes[1].plot(simulink_subset['Iteration'], simulink_subset['Execution Time (s)'], label=f'simulink, $F_S$: {freq:.0e}', marker='.')

axes[1].set_title('b.')
axes[1].set_xlabel('Iteration')
axes[1].set_ylabel('Execution Time (s)')
axes[1].legend(loc='upper left', bbox_to_anchor=(0, 0.87))
#axes[1].legend()

# Plot 3: Memory Usage (Average & Peak) vs Sampling Frequency
axes[2].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Average Memory Usage (MiB)', 'mean')], label='pyblksim, Avg', marker='x')
axes[2].plot(pyblksim_summary['Sampling Frequency (Hz)'], pyblksim_summary[('Average Memory Usage (MiB)', 'max')], label='pyblksim, Peak', marker='x')
axes[2].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Average Memory Usage (MiB)', 'mean')], label='simulink, Avg', marker='.')
axes[2].plot(simulink_summary['Sampling Frequency (Hz)'], simulink_summary[('Average Memory Usage (MiB)', 'max')], label='simulink, Peak', marker='.')
axes[2].set_title('c.')
axes[2].set_xlabel('$F_S$: Sampling Frequency (Hz)')
axes[2].set_ylabel('Memory Usage (MiB)')
axes[2].legend()

# Filter pyblksim data to include only the sampling frequencies that are present in bdsim data
filtered_pyblksim_summary = pyblksim_summary[pyblksim_summary['Sampling Frequency (Hz)'].isin(bdsim_summary['Sampling Frequency (Hz)'])]

# Plot 4: bdsim and filtered pyblksim Execution Time and Memory Usage vs Sampling Frequency with separate y-axes
ax4_1 = axes[3]
ax4_2 = ax4_1.twinx()

# bdsim data
ax4_1.plot(bdsim_summary['Sampling Frequency (Hz)'], bdsim_summary[('Execution Time (s)', 'mean')], label='bdsim Execution Time', marker='.', color='b')
ax4_2.plot(bdsim_summary['Sampling Frequency (Hz)'], bdsim_summary[('Average Memory Usage (MiB)', 'mean')], label='bdsim Memory Usage', marker='.', color='r')

# filtered pyblksim data
ax4_1.plot(filtered_pyblksim_summary['Sampling Frequency (Hz)'], filtered_pyblksim_summary[('Execution Time (s)', 'mean')], label='pyblksim Execution Time', marker='x', color='b')
ax4_2.plot(filtered_pyblksim_summary['Sampling Frequency (Hz)'], filtered_pyblksim_summary[('Average Memory Usage (MiB)', 'mean')], label='pyblksim Memory Usage', marker='x', color='r')

ax4_1.set_xlabel('$F_S$: Sampling Frequency (Hz)')
ax4_1.set_ylabel('Execution Time (s)', color='b')
ax4_2.set_ylabel('Memory Usage (MiB)', color='r')

# Move the legends to the top left corner
ax4_1.legend(loc='upper left')
ax4_2.legend(loc='upper left', bbox_to_anchor=(0, 0.9))
ax4_1.set_title('d.')

plt.tight_layout()
plt.show()
