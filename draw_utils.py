import matplotlib.pyplot as plt
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
i = 0
for frame in videoreader:
    
    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(frame)
    
    # Find x, y, width, height of each frame
    if len(use_data[i]) > 0:
        x = use_data[i]['x']
        y = use_data[i]['y']
        width = use_data[i]['width']
        height = use_data[i]['height']
        # Create a Rectangle patch
        rect = plt.Rectangle((x,y),width,height,linewidth=1,edgecolor='r',facecolor='none')
    
        # Add the patch to the Axes
        ax.add_patch(rect)
        
    i += 1
    plt.show()