from retrieve_utils import BodyReader, VideoReader, BallReader
from draw_utils import draw_frame

import cv2
import os
import argparse

from time import sleep

def main(data_path, video_path, out_path):
    videoname = video_path.split('/')[-1]

    videoreader = VideoReader(video_path)
    bodyreader = BodyReader(f'{data_path}/keypoints.json', videoname)
    ballreader = BallReader(f'{data_path}/balls.json', videoname)

    if out_path:
        output = cv2.VideoWriter(out_path, -1, 20.0, (640,480))

    for frame, ball, body in zip(videoreader, ballreader, bodyreader):
        frame = draw_frame(frame, ball, body)
        cv2.imshow('Are We Still Juggling?', frame)

        if out_path:
            output.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(0.016)
    
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