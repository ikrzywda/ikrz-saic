import numpy as np
import matplotlib.pyplot as plt


ltspice_sim_output_path = 'integrating-circuit.txt' 
with open(ltspice_sim_output_path, 'r', encoding='latin1') as file:
    lines = file.readlines()

# Extract frequency, magnitude, and phase from the data
frequency = []
magnitude = []
phase = []
for line in lines[1:]:  # Skip the header
    parts = line.split()
    frequency.append(float(parts[0]))
    mag_phase_str = parts[1].split(',')
    magnitude.append(float(mag_phase_str[0][1:-2]))
    phase.append(float(mag_phase_str[1][:-2]))

# Plotting phase versus frequency
plt.figure(figsize=(10, 6))
plt.semilogx(frequency, phase, marker='o', linestyle='-')
plt.title('Phase vs. Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (degrees)')
plt.grid(True)
plt.show()

# Plotting amplitude versus frequency
plt.figure(figsize=(10, 6))
plt.semilogx(frequency, magnitude, marker='o', linestyle='-')
plt.title('Amplitude vs. Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.show()

