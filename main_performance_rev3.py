import time
import memory_profiler
import numpy as np
import matplotlib.pyplot as plt
import os
import matlab.engine
import bdsim
from pyblksim.common.sources import SquareWave, SineWave
from pyblksim.common.sinks import Scope
from pyblksim.sims.basics import Environment
import csv

def simulink(fs, matlab_executable_path=None):
    simulink_file_path = "./simulink_performance_eval.slx"
    block_paths = ["simulink_performance_eval/Pulse Generator","simulink_performance_eval/Sine Wave"]
    error_message = None

    try:
        # Check if the file exists
        if not os.path.isfile(simulink_file_path):
            raise FileNotFoundError(f"Simulink model file not found: {simulink_file_path}")

        # Start the MATLAB engine
        if matlab_executable_path:
            eng = matlab.engine.start_matlab(executable=matlab_executable_path)
        else:
            eng = matlab.engine.start_matlab()

        # Clearing workspace
        eng.eval("clear all", nargout=0)
        # Open the Simulink model
        eng.eval(f"open('{simulink_file_path}');", nargout=0)

        # Set the sample time for each block
        for block_path in block_paths:
            eng.set_param(block_path, "SampleTime", str(1/fs), nargout=0)

        # Run the simulation
        eng.eval(f"sim('{simulink_file_path}');", nargout=0)

    except Exception as e:
        error_message = f"Error running Simulink model: {e}"

    # Close the MATLAB engine
    finally:
        if 'eng' in locals():
            eng.quit()

    return error_message

def bdsim_simulation(fs):
    # Create a BDSim instance (inside the function for reusability)
    sim = bdsim.BDSim()

    # Create a block diagram
    bd = sim.blockdiagram()

    # Define simulation parameters based on fs
    TSIM = 5  # in seconds
    dt = 1 / fs  # Sampling time based on fs

    # Create waveforms (assuming FS is not used)
    square_wave = bd.WAVEFORM(wave='square', freq=1, amplitude=5, offset=0, duty=0.5)
    sine_wave = bd.WAVEFORM(wave='sine', freq=1, amplitude=5, offset=0)

    # Create scopes for each waveform
    square_scope = bd.SCOPE()
    sine_scope = bd.SCOPE()

    # Connect sources to scopes
    bd.connect(square_wave, square_scope)
    bd.connect(sine_wave, sine_scope)

    # Compile the block diagram
    bd.compile()

    # Run the simulation
    results = sim.run(bd, T=TSIM, dt=dt, block=False)
    return results

def pyblksim_simulation(fs):
        
    # User settings
    TSIM = 5  # Simulation time in seconds

    # Create simulation environment
    env = Environment.init()

    # Create a square wave source
    square_wave = SquareWave(env, offset=0, amplitude=5, frequency=1, sampling_frequency=fs, duty_cycle=0.5)

    # Create a sine wave source
    sine_wave = SineWave(env, amplitude=5, frequency=1, sampling_frequency=fs)

    # Create scopes to observe the waves
    square_scope = Scope(env, sampling_frequency=fs, name="Square Wave Scope")
    sine_scope = Scope(env, sampling_frequency=fs, name="Sine Wave Scope")

    # Connect sources to scopes and CSV sinks
    square_scope.input = square_wave.output
    sine_scope.input = sine_wave.output

    # Run the simulation
    env.run(until=TSIM)

def measure_performance(script, fs, n):
    execution_times = []
    peak_memory_usages = []
    avg_memory_usages = []

    for i in range(n):
        # Measure start time
        start_time = time.time()

        # Profile memory usage
        if script == 'simulink':
            mem_usage = memory_profiler.memory_usage(lambda: simulink(fs), interval=0.1, timeout=None, include_children=True)
        elif script == 'bdsim':
            mem_usage = memory_profiler.memory_usage(lambda: bdsim_simulation(fs), interval=0.1, timeout=None, include_children=True)
        elif script == 'pyblksim':
            mem_usage = memory_profiler.memory_usage(lambda: pyblksim_simulation(fs), interval=0.1, timeout=None, include_children=True)

        end_time = time.time()

        # Calculate execution time, peak memory usage, and average memory usage
        execution_time = end_time - start_time
        peak_memory = max(mem_usage)
        avg_memory = sum(mem_usage) / len(mem_usage)
        
        execution_times.append(execution_time)
        peak_memory_usages.append(peak_memory)
        avg_memory_usages.append(avg_memory)
        
    return execution_times, peak_memory_usages, avg_memory_usages

if __name__ == "__main__":
    # Choose desired sampling frequencies 
    script_values = ['pyblksim', 'simulink', 'bdsim']    
    fs_values = np.logspace(np.log10(1e3), np.log10(2500000), num=10, base=10).astype(int).tolist()
    n = 10  # Number of iterations per sampling frequency

    for script in script_values:
        # Write headers to CSV
        headers = ['Script', 'Sampling Frequency (Hz)', 'Iteration', 'Execution Time (s)', 'Peak Memory Usage (MiB)', 'Average Memory Usage (MiB)']
        csv_file = f'performance_results_{script}.csv'
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

        for fs in fs_values:
            exec_times, peak_mem_usages, avg_mem_usages = measure_performance(script, fs, n)

            for i in range(n):
                result = [script, fs, i + 1, exec_times[i], peak_mem_usages[i], avg_mem_usages[i]]
                print(f'\nSimulation of {script} with sampling frequency {fs} Hz (iteration {i + 1}):')
                print(f"Execution time: {exec_times[i]} seconds")
                print(f"Peak memory usage: {peak_mem_usages[i]} MiB")
                print(f"Average memory usage: {avg_mem_usages[i]} MiB\n")

                # Append results to CSV file
                with open(csv_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(result)
