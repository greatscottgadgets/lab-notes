#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import sys

def parse_point(line):
    line = line.rstrip()
    x, y = line.split(',')
    return (float(x) * 1e9, float(y))

for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        data = f.readlines()
        points = [parse_point(line) for line in data[18:]]
        x, y = np.array(points).T
        label = f"{filename[3:-4]} mil"
        plt.plot(x, y, label=label)

ax = plt.gca()
ax.legend()
ax.set_xlim(None, 8.5)
ax.set_ylim(40, 65)

plt.xlabel('Time (ps)')
plt.ylabel('Impedance (Ohm)')
plt.minorticks_on()
plt.grid(which='major')
plt.grid(which='minor', alpha=0.2)

plt.show()
