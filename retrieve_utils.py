import imageio
import json
import numpy as np
import cv2

class BodyReader:
    ''' Load keypoint data of body parts per frame and process them for easy use. ''' 
    def __init__(self, data_path, video_name):
        # Initialize video by name and data file
        self.data_path = data_path 
        self.video_name = ''.join(video_name.split('.')[:-1])

        with open(self.data_path) as f:
            self.data = json.load(f)[self.video_name]
        
        self.max_frame = int(len(self.data) - 1)

    def __iter__(self):
        # Create iterator
        self.cur_frame = 0
        return self

    def __next__(self):
        # Iterate over frames and retrieve keypoint data if present
        if self.cur_frame < self.max_frame:
            if self.data[str(self.cur_frame)]['LAnkle']['x'] != -1 and self.data[str(self.cur_frame)]['RAnkle']['x'] != -1:
                result = self.data[str(self.cur_frame)]
            elif self.data[str(self.cur_frame)]['LAnkle']['x'] != -1 and self.data[str(self.cur_frame)]['RAnkle']['x'] == -1:
                self.data[str(self.cur_frame)]['RAnkle'] = {}
                result = self.data[str(self.cur_frame)]
            elif self.data[str(self.cur_frame)]['LAnkle']['x'] == -1 and self.data[str(self.cur_frame)]['RAnkle']['x'] != -1: 
                self.data[str(self.cur_frame)]['LAnkle'] = {}
                result = self.data[str(self.cur_frame)]
            else:
                result = {}
            self.cur_frame += 1
            return result
        else:
            raise StopIteration

class BallReader:
    ''' Load ball data per frame and process them for easy use. ''' 
    def __init__(self, data_path, video_name):
        # Initialize video by name and data file
        self.data_path = data_path
        self.video_name = video_name

        with open(self.data_path) as f:
            self.data = json.load(f)[self.video_name]
        
        self.max_frame = int(len(self.data) - 1)
        
    def __iter__(self):
        # Create iterator
        self.cur_frame = 0
        return self

    def __next__(self):
        # Iterate over frames and retrieve location of the ball if present
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
    ''' Retrieve data for specific video and determine the amount of frames '''
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.shape = (int(width), int(height))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

    def __iter__(self):
        self.cur_frame = 0
        return self

    def __next__(self):
        if self.cur_frame < self.total_frames:
            self.cur_frame += 1

            return self.video.read()
        else:
            raise StopIteration

    def __delete__(self, video):
        del(self.video)