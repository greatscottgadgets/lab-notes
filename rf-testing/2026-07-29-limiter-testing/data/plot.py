import numpy as np
import skrf
import sys

from matplotlib import pyplot as plt
from matplotlib import style

plot_data = []
for file in sys.argv[1:]:
    ts = skrf.Touchstone(file)
    data = ts.get_sparameter_arrays()
    power_in = data[0] / ts.frequency_mult
    s21 = data[1]
    gain = 20*np.log10(np.abs(s21).flatten())
    power_out = power_in + gain

    plot_data.append([file, power_in, power_out])

# Sort by last value in power_out, so legend order matches trace order
for data in  sorted(plot_data, key=lambda d: d[2][-1], reverse=True):
    plt.plot(data[1], data[2], label=data[0])

plt.title('Limiter Test - Power Sweep @ 425 MHz CW')
plt.xlabel('Power in (dBm)')
plt.ylabel('Power out (dBm)')
plt.xticks(range(31), minor=True)
plt.yticks(range(31), minor=True)
plt.grid(True, 'major')
plt.grid(True, 'minor', alpha=0.3)

legend = plt.legend()
for handle in legend.legend_handles:
    handle.set_linewidth(3.0)
plt.show()
