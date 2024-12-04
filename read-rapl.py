import os
import time

cpu_rapl_path = '/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj'

try:
    with open(cpu_rapl_path, 'r') as file:
        initial_value = int(file.read().strip())
except FileNotFoundError:
    print(f"Error: {cpu_rapl_path} not found. Ensure you have the correct path and permissions.")
    exit(1)
except PermissionError:
    print(f"Error: Permission denied when accessing {cpu_rapl_path}.")
    exit(1)

# Compile the Java program
compilation_status = os.system("javac MathServer.java")
if compilation_status != 0:
    print("Error: Failed to compile MathServer.java")
    exit(1)

# Run the Java program
execution_status = os.system("java MathServer")
if execution_status != 0:
    print("Error: Failed to execute MathServer")
    exit(1)

# Sleep for a short duration to allow the program to run
time.sleep(1)

try:
    with open(cpu_rapl_path, 'r') as file:
        final_value = int(file.read().strip())
except FileNotFoundError:
    print(f"Error: {cpu_rapl_path} not found. Ensure you have the correct path and permissions.")
    exit(1)
except PermissionError:
    print(f"Error: Permission denied when accessing {cpu_rapl_path}.")
    exit(1)

# Calculate energy consumption in Joules
energy_consumption = (final_value - initial_value) / 1_000_000  # Convert from microjoules to joules

print("Energy consumption (Joules):", energy_consumption)

