import imageio
from PIL import Image
import json
import numpy as np
import cv2
from retrieve_utils import BallReader
from retrieve_utils import VideoReader

# Read each frame
videoreader = VideoReader('data/j.mp4')

# Create a list from the data of the ball
data_vid = BallReader('balls.json', 'j.mp4')
use_data = []
for ball_data in data_vid:
    use_data.append(ball_data)

# Draw a square around the ball in each frame given the data
# Draw a square around the ball in each frame given the data
i = 0
for frame in videoreader:
    
    # Find x, y, width, height of each frame
    if len(use_data[i]) > 0:
        x = use_data[i]['x']
        y = use_data[i]['y']
        width = use_data[i]['width']
        height = use_data[i]['height']
        # Create a Rectangle patch
        color = (0, 0, 255)
        thickness = 2
        
        frame = cv2.rectangle(frame, (x, y), (x+width, y+height), color, thickness)
        
    cv2.imshow("image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    i += 1
    break