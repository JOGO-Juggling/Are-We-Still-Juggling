from retrieve_utils import BodyReader, VideoReader
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(111)

videoreader = VideoReader('data/videos/0f7aa7cb9bf54f8ca89d551ecdccc735.MOV')
bodyreader = BodyReader('data/keypoints.json', '0f7aa7cb9bf54f8ca89d551ecdccc735.MOV')
frames = []

for i, (frame, keypoints) in enumerate(zip(videoreader, bodyreader)):
    result = [ax.imshow(frame, animated=True)]
    if keypoints != {}:
        if keypoints['RAnkle'] != {}:
            x, y = int(keypoints['RAnkle']['x']), int(keypoints['RAnkle']['y'])
            circle = patches.Circle((x, y), 20, color='r')
            result.append(ax.add_patch(circle))
        if keypoints['LAnkle'] != {}:
            x, y = int(keypoints['LAnkle']['x']), int(keypoints['LAnkle']['y'])
            circle = patches.Circle((x, y), 20, color='g')
            result.append(ax.add_patch(circle))
    frames.append(result)

animation = animation.ArtistAnimation(fig, frames, interval=32)
animation.save('result.mp4')
# plt.show()