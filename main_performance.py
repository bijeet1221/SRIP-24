import time
import memory_profiler
import numpy as np
import matplotlib.pyplot as plt
import os
import matlab.engine
import bdsim
from pyblksim.common.sources import SquareWave, SineWave, BandLimitedWhiteNoise
from pyblksim.common.sinks import Scope, ToCSV
from pyblksim.sims.basics import Environment
import csv





def simulink(fs, matlab_executable_path=None):
  
    simulink_file_path = ".\simulink_performance_eval.slx"
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

    # Plot the results
    square_scope.plot()
    sine_scope.plot()



def measure_performance(script, fs, n):
   
    total_time = 0
    total_memory = 0

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

        # Calculate execution time and peak memory usage
        execution_time = end_time - start_time
        peak_memory = max(mem_usage)
        total_time += execution_time
        total_memory += peak_memory
        
    avg_runtime = total_time / n
    avg_memory = total_memory / n

    return (avg_runtime,avg_memory)


if __name__ == "__main__":
    # Choose desired sampling frequencies 
    #script_values = ['simulink_closed', 'simulink_open', 'bdsim_performance_eval_example', 'pyblksim_performance_eval_example']
    script_values = ['simulink']
    fs_values = [1000, 2000] #, 4000, 8000, 16000]
    n = 1
    Runtime = []
    Net_Memory = []

    for script in script_values:
    
        local_runtime = []
        local_memory = []

        for fs in fs_values:
            # Call run_simulation and measure performance
            exec_time, peak_mem = measure_performance(script, fs, n)
            local_runtime.append(exec_time)
            local_memory.append(peak_mem)

            # Print results for each sampling frequency
            print(f'\nSimulation of {script}')
            print(f"Simulation with sampling frequency {fs} Hz:")
            print(f"Average Execution time for {n} runs: {exec_time} seconds")
            print(f"Average Peak memory usage for {n} runs: {peak_mem} MiB\n")

        Runtime.append(local_runtime)
        Net_Memory.append(local_memory)
    
    transposed_runtime = list(zip(*Runtime))
    transposed_memory = list(zip(*Net_Memory))
    
    with open('runtime_vs_frequency.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(transposed_runtime)

    with open('memory_vs_frequency.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(transposed_memory)
