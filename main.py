from retrieve_utils import BodyReader, VideoReader, BallReader
from draw_utils import draw_frame

import cv2
import os
import argparse

from time import sleep

def calc_dy(prev_y, curr_y):
    return curr_y - prev_y

def main(data_path, video_path, out_path):
    videoname = video_path.split('/')[-1]

    # Open video and datastreams
    videoreader = VideoReader(video_path)
    bodyreader = BodyReader(f'{data_path}/keypoints.json', videoname)
    ballreader = BallReader(f'{data_path}/balls.json', videoname)

    # Set output if needed
    if out_path:
        output = cv2.VideoWriter(out_path, -1, 20.0, (640,480))
    
    prev_ball_y = 0

    # Loop over datastreams
    for frame, ball, body in zip(videoreader, ballreader, bodyreader):
        # Calculate vertical ball trajectory
        if ball != {}:
            ball_dy = calc_dy(prev_ball_y, ball['y'])
            prev_ball_y = ball['y']

        # Draw frame
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = draw_frame(frame, ball, body, ball_dy)
        cv2.imshow('Are We Still Juggling?', frame)

        if out_path:
            output.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(0.032)
    
    if out_path:
        output.release()
    cv2.destroyAllWindows()

def dir_type(path):
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)

def file_type(path):
    if os.path.isfile(path):
        return path
    else:
        raise FileNotFoundError(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process juggling videos.')
    parser.add_argument('--data', type=dir_type, required=True,
                        help='Path to the data directory', metavar='DIR')
    parser.add_argument('--video', type=file_type, required=True,
                        help='Path to the video in the data dir.', metavar='FILE')
    parser.add_argument('--output', type=file_type, required=False,
                        help='Path to the output video.', metavar='FILE')

    args = parser.parse_args()
    main(args.data, args.video, args.output)