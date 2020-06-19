from retrieve_utils import BodyReader, VideoReader, BallReader
from draw_utils import draw_frame

import cv2
import os
import argparse
import numpy as np

import time
from time import sleep
from math import hypot

TRAJECTORY_LEN = 3

def process_ball_trajectory(ball_traj):
    '''Detect bounces in the ball trajectory'''

    # Calculate dy over measured trajectory
    y_trajectory = [ball['y'] for ball in ball_traj if ball != {}]
    dy_trajectory = [y - py for y, py in zip(y_trajectory[:-1], y_trajectory[1:])]

    # Detect if the dy 'goes trough zero'
    change = np.where(np.diff(np.sign(dy_trajectory)))[0]
    return (len(change) > 0 and dy_trajectory[0] < 0)

def process_bounce(ball_traj, body_traj, frame_shape):
    '''Given the trajectory of the ball and the body during a bounce,
    determines whether the ball bounces on the ground or a body part.'''

    threshold = 0.15

    try:
        ball = ball_traj[0]
        r_ankle = body_traj[0]['RAnkle']
        l_ankle = body_traj[0]['LAnkle']

        ball_x = ball['x'] + 0.5 * ball['width']
        ball_y = ball['y'] + 0.5 * ball['height']

        ball_norm = np.divide((ball_x, ball_y), frame_shape)
        r_ankle_norm = np.divide((r_ankle['x'], r_ankle['y']), frame_shape)
        l_ankle_norm = np.divide((l_ankle['x'], l_ankle['y']), frame_shape)

        r_dist = hypot(ball_norm[0] - r_ankle_norm[0], ball_norm[1] - r_ankle_norm[1])
        l_dist = hypot(ball_norm[0] - l_ankle_norm[0], ball_norm[1] - l_ankle_norm[1])

        dists = [r_dist, l_dist]
        min_dist = np.argmin(dists)

        if dists[min_dist] < threshold:
            return min_dist + 1, 1 - dists[min_dist] / threshold
        return 0, 1 - dists[min_dist] / threshold
    except:
        return 0, 0

def main(data_path, video_path, out_path, display=True, true_time=True):
    videoname = video_path.split('/')[-1]

    # Open video and datastreams
    videoreader = VideoReader(video_path)
    bodyreader = BodyReader(f'{data_path}/keypoints.json', videoname)
    ballreader = BallReader(f'{data_path}/balls.json', videoname)
    frame_shape = videoreader.shape
    fps = videoreader.fps

    # Set output if needed
    if out_path:
        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        output = cv2.VideoWriter(out_path, fourcc, fps, frame_shape)
    
    # Setup trajectories
    ball_trajectory = [{}] * TRAJECTORY_LEN
    body_trajectory = [{}] * TRAJECTORY_LEN

    prev_ball = []

    bounce = False
    confidence = 0.0
    foot = 0

    ball_dy = 0

    start_time = time.time()
    bounces = 0

    juggling = True

    # Loop over datastreams
    for frame, ball, body in zip(videoreader, ballreader, bodyreader):
        ball_trajectory.pop(0)
        body_trajectory.pop(0)

        if len(ball) > 0:
            prev_ball = ball
        
        if len(ball) is 0:
            ball_trajectory.append(prev_ball)
        else:
            ball_trajectory.append(ball)
        
        body_trajectory.append(body)

        bounce = process_ball_trajectory(ball_trajectory)

        if bounce:
            bounce_check = True
            bounces += 1
            
            foot, confidence = process_bounce(ball_trajectory, body_trajectory, frame_shape)

            if foot is 0:
                juggling = False
            else:
                juggling = True
        else:
            foot = 0

        # Draw frame
        if display or out_path:
            if ball != {} and ball_trajectory[-1] != {}:
                ball_dy = ball['y'] - ball_trajectory[-1]['y']

            frame = frame[1]
            frame = draw_frame(frame, ball, body, ball_dy, foot, juggling, confidence)

            # Draw frame to screen
            if display:
                cv2.imshow('Are We Still Juggling?', frame)

                if true_time:
                    sleep(int(1000 / fps) / 1000)
            
            # Draw frame to output
            if out_path:
                frame = cv2.resize(frame, frame_shape)
                output.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    exec_time = (time.time() - start_time) * 1000
    exec_time_per_frame = exec_time / videoreader.total_frames

    print(f'Total execution time: {exec_time}ms')
    print(f'Average execution time per frame: {exec_time_per_frame}ms')
    
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
    parser.add_argument('--output', type=str, required=False,
                        help='Path to the output video.', metavar='FILE')
    parser.add_argument('--display', type=bool, required=False,
                        help='Set output to on or off.')
    parser.add_argument('--truetime', type=bool, required=False, default=False,
                        help='Maximize FPS or use video FPS')
    args = parser.parse_args()

    if not args.display:
        args.truetime = False
    main(args.data, args.video, args.output, args.display, args.truetime)