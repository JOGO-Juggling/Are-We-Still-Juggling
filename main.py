from retrieve_utils import BodyReader, VideoReader, BallReader
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(111)

video = '0f272d8bfd2947a0b37f0deaf2fe20bd.MOV'
videoreader = VideoReader(f'data/videos/{video}')
bodyreader = BodyReader('data/keypoints.json', video)
ballreader = BallReader('data/balls.json', video)
frames = []

for i, (frame, keypoints, ball) in enumerate(zip(videoreader, bodyreader, ballreader)):
    result = [ax.imshow(frame, animated=True)]
    if keypoints != {}:
        if keypoints['RAnkle'] != {}:
            x, y = int(keypoints['RAnkle']['x']), int(keypoints['RAnkle']['y'])
            circle = patches.Circle((x, y), 10, color='r')
            result.append(ax.add_patch(circle))
        if keypoints['LAnkle'] != {}:
            x, y = int(keypoints['LAnkle']['x']), int(keypoints['LAnkle']['y'])
            circle = patches.Circle((x, y), 10, color='g')
            result.append(ax.add_patch(circle))
    if ball != {}:
        x, y = int(ball['x']), int(ball['y'])
        w, h = int(ball['width']), int(ball['height'])
        square = patches.Rectangle((x, y), w, h, )
        result.append(ax.add_patch(square))
    frames.append(result)

animation = animation.ArtistAnimation(fig, frames, interval=32)
animation.save('result.mp4')
# plt.show()