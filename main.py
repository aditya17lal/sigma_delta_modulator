import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Get simulation parameters from user input; fs,f0=200,40 for example
fs = float(input("Enter sampling rate (in Hz): "))
T = 0.7  # total time in seconds
f0 = float(input("Enter frequency of input (in Hz): "))
Vref = 1  # reference voltage
N = int(fs * T)  # number of samples

# Define initial values
v1 = 0  # integrator output
v_quant = 0  # quantizer output
out = np.zeros(N)  # modulator output

# Generate input signal
t = np.linspace(0, T, N)
x = np.cos(2 * np.pi * f0 * t)

# Perform sigma-delta modulation
for n in range(N):
    v = x[n] - v1  # subtract integrator output from input
    if v > 0:
        v_quant = Vref  # output high if input > v1
    else:
        v_quant = -Vref  # output low if input <= v1
    out[n] = v_quant  # save modulator output
    v1 += v_quant / Vref  # update integrator output
    shifted_t = t + (1 / (4 * f0))

# Define the low-pass filter
fc = f0  # cutoff frequency
b, a = signal.butter(2, 2 * fc / fs, 'low')

# Calculate scaling factor based on fs and f0
scale_factor = np.pi * f0 / fs

# Filter the modulator output to obtain the demodulated signal
demod = signal.lfilter(b, a, out) * (Vref / scale_factor)  # scale to match input amplitude

# Set up subplots with some space
fig, axs = plt.subplots(3, 1, figsize=(10, 18), gridspec_kw={'hspace': 1})

# Plot input
axs[0].plot(t, x, color='blue', label='Input')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Amplitude')
axs[0].set_title('Input Signal')

# Plot modulated output
axs[1].step(shifted_t, out, where='post', color='red', label='Modulated Output')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('Modulated Output')

# Plot demodulated output
axs[2].plot(t, demod, color='green', label='Demodulated Output')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Amplitude')
axs[2].set_title('Demodulated Output')

plt.tight_layout()
plt.show()
