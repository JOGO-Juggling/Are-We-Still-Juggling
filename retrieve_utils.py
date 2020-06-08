import imageio
import json
import numpy as np

def get_body_part_bboxes(video_path):
    pass


class BallReader:
    def __init__(self, data_path, video_name):
        self.data_path = data_path
        self.video_name = video_name

        with open(self.data_path) as f:
            self.data = json.load(f)[self.video_name]
        
        self.max_frame = int(len(self.data) - 1)
    
    def __iter__(self):
        self.cur_frame = 0
        return self

    def __next__(self):
        if self.cur_frame < self.max_frame:
            if len(self.data[str(self.cur_frame)]) > 0:
                del(self.data[str(self.cur_frame)][0]['confidence'])
                result = self.data[str(self.cur_frame)][0]
            else:
                result = {}
            self.cur_frame += 1
            return result
        else:
            raise StopIteration

class VideoReader:
    def __init__(self, video_path):
        self.video = imageio.get_reader(video_path)
        self.total_frames = self.video.count_frames()
    
    def __iter__(self):
        self.cur_frame = 0
        return self

    def __next__(self):
        if self.cur_frame < self.total_frames:
            im = self.video.get_data(self.cur_frame)
            self.cur_frame += 1

            return im
        else:
            raise StopIteration

    def __delete__(self, video):
        del(self.video)


# # VideoReader iterable test
# videoreader = VideoReader('data/j.mp4')
# for frame in videoreader:
#     print(frame)
#     break

# # BallReader iterable test
# ballreader = BallReader('data/balls.json', 'j.mp4')
# for frame in ballreader:
#     print(frame)