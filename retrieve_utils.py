import imageio
import json
import numpy as np

def get_body_part_bboxes(video_path):
    pass

def get_ball_bboxes(video_name, data_path):
    with open(data_path) as f:
        data = json.load(f)

    frames = []
    for i in range(int(len(data[video_name]) - 1)):
        if len(data[video_name][str(i)]) > 0:
            del(data[video_name][str(i)][0]['confidence'])
            frames.append(data[video_name][str(i)][0])
        else:
            empty_dict = {}
            frames.append(empty_dict)

    return frames

def get_frames(video_path):
    video = imageio.get_reader(video_path)
    total_frames = video.count_frames()
    frames = []

    for i in range(total_frames):
        im = video.get_data(i)
        frames.append(im)
            
    return frames


# print(get_ball_bboxes('j.mp4', 'data/balls.json'))
