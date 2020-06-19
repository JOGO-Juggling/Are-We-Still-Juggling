from retrieve_utils import BallReader
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

ball_traj = BallReader('data/balls.json', '0f272d8bfd2947a0b37f0deaf2fe20bd.MOV')

def interpolate(ball_traj):
    y_trajectory = [ball['y'] if ball != {} else 0 for ball in ball_traj]

    y_values = []
    y_index = []
    for i, y in enumerate(y_trajectory):
        if y != -1:
            y_values.append(y)
            y_index.append(i)
    
    inter = interp1d(y_index, y_values, kind='cubic')
    new_x = np.linspace(min(y_index), max(y_index), num=50)
    plt.plot(new_x, inter(new_x))
    plt.show()

ball_hist = [{}] * 10
for ball in ball_traj:
    ball_hist.pop(0)
    ball_hist.append(ball)
    interpolate(ball_hist)