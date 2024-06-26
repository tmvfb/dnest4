import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Execute the kepler.py script using system command
subprocess.run(["python3", "kepler.py"])

# Load all the files
trajectories = []
for i in range(1, 122):
    v = 0.4 + 0.005 * (i - 1)
    print(v)
    filename = f"orbits{v:.3f}.dat"
    trajectory = np.loadtxt(filename)
    trajectories.append(trajectory)

def evaluate(arg_to_sin, v=0.75, viewing_angle=0.):
    # Which trajectory to use?
    orbit = int(np.floor((v - 0.4) / 0.005)) + 1
    N = trajectories[orbit - 1].shape[0]

    radial_velocity = np.cos(viewing_angle) * trajectories[orbit - 1][:, 0] + np.sin(viewing_angle) * trajectories[orbit - 1][:, 1]
    radial_velocity /= np.max(np.abs(radial_velocity))
    radial_velocity = (radial_velocity - np.min(radial_velocity)) / (np.max(radial_velocity) - np.min(radial_velocity))
    radial_velocity = 2 * radial_velocity - 1
    closest_to_max = np.where(radial_velocity == np.max(radial_velocity))[0][0]

    cc = 2 * np.pi * (closest_to_max - 1) / N
    index = 1 + N * ((arg_to_sin + cc) % (2 * np.pi)) / (2 * np.pi)

    return radial_velocity[int(index)]

t = np.arange(0, 10, 0.01)
y = [evaluate(2 * np.pi * ti / 5 + 2.2, v=np.sqrt(1. - 0.5), viewing_angle=-2.7) for ti in t]
plt.plot(t, y)

data = pd.read_csv("kepler.txt", sep=" ", header=None)
plt.plot(data.iloc[:, 0], data.iloc[:, 1])

plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Plot of y vs t and data from kepler.txt')
plt.legend(['y vs t', 'Data from kepler.txt'])
plt.grid(True)
plt.show()
