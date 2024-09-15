# README

## Overview
This repository contains a collection of Python scripts designed to compare the performance of various discrete time simulators, including **PyblkSim**, **MATLAB/Simulink**, and **BDSim**. The goal of this project is to evaluate the runtime and memory usage of these simulators when processing different signal types such as square waves, sine waves, and band-limited noise, with varying sampling frequencies.

## Key Features
- **Performance Comparison**: Measures the average execution time and memory usage for each simulator.
- **Simulation Types**: Includes support for multiple simulation types, such as square waves and sine waves.
- **Simulator Support**:
  - **PyblkSim**: A Python-based discrete time simulator.
  - **MATLAB/Simulink**: A widely used tool for modeling and simulating dynamic systems.
  - **BDSim**: A block diagram simulation tool built with Python.

## Files and Structure

- `performance_eval.py`: A core script that initiates simulations in different environments (PyblkSim, Simulink, BDSim) and measures their performance.
- `simulink_performance_eval.slx`: The Simulink model used in the simulation comparisons.
- CSV Output: Simulation results, including runtime and memory performance metrics, are saved in CSV format.

## How to Use

### Requirements
To run the scripts, you'll need to have the following libraries and tools installed:
- `numpy`
- `matplotlib`
- `memory_profiler`
- `bdsim`
- `pyblksim`
- `matlab.engine` (MATLAB must be installed for Simulink support)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/performance-eval-simulators.git
    cd performance-eval-simulators
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that MATLAB is installed and accessible via the `matlab.engine` Python package.

### Running the Simulations

1. To evaluate the performance of different simulators, edit the sampling frequencies (`fs_values`) and the number of iterations (`n`) in the main script (`performance_eval.py`).
   
2. Run the script:
    ```bash
    python performance_eval.py
    ```

3. The results, including execution time and memory usage for each simulator, will be printed to the console and saved as CSV files (e.g., `runtime_vs_frequency.csv`, `memory_vs_frequency.csv`, `performance_results_<simulator>.csv`).

### Customization

- **Simulink File**: You can modify the Simulink model (`simulink_performance_eval.slx`) to test other signal types or block configurations.
- **Sampling Frequencies**: Update the `fs_values` list to adjust the sample rates for the simulations.
- **Simulators**: You can add new simulators or customize the existing ones by editing the respective functions (`simulink()`, `bdsim_simulation()`, `pyblksim_simulation()`).

## Performance Metrics
For each simulation, the following metrics are captured:
- **Execution Time**: Average time taken for each simulation run.
- **Peak Memory Usage**: Maximum memory used during the simulation.
- **Average Memory Usage**: Average memory consumption over the course of the simulation.

## Results
Results for each script (PyblkSim, Simulink, BDSim) are stored in separate CSV files (`performance_results_<simulator>.csv`) and include the following columns:
- Script name
- Sampling frequency (Hz)
- Iteration number
- Execution time (seconds)
- Peak memory usage (MiB)
- Average memory usage (MiB)

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Contact
For any inquiries or issues, please reach out to [Bijeet.Basak@iiitb.ac.in].

---
