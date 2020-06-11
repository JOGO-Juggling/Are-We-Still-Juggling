from retrieve_utils import BodyReader, VideoReader, BallReader
from draw_utils import draw_frame

import cv2
import os
import argparse
import numpy as np

import time
from time import sleep

TRAJECTORY_LEN = 4

def process_ball_trajectory(ball_traj):
    '''Detect bounces in the ball trajectory'''

    # Calculate dy over measured trajectory
    y_trajectory = [ball['y'] for ball in ball_traj if ball != {}]
    dy_trajectory = [dy - pdy for dy, pdy in zip(y_trajectory[:-1], y_trajectory[1:])]

    # Detect if the dy 'goes trough zero'
    change = np.where(np.diff(np.sign(dy_trajectory)))[0]
    return len(change) > 0 and dy_trajectory[0] < 0, change

def process_bounce(ball_traj, body_traj):
    '''Given the trajectory of the ball and the body during a bounce,
    determines whether the ball bounces on the ground or a body part.'''

    threshold = 0.5
    min_frame = np.argmin(ball_traj)

    ball_min, body_min = ball_traj[min_frame], body_traj[min_frame]

    l_body = (body_min['LAnkle']['x'], body_min['LAnkle']['y'])
    r_body = (body_min['RAnkle']['x'], body_min['RAnkle']['y']) 

    ball_pos = (ball_min['x'], ball_min['y'])

    if np.linalg.norm([ball_pos, l_body ]) < threshold or np.linalg.norm([ball_pos, r_body ]) < threshold:
        return True
    else:
        return False

def main(data_path, video_path, out_path, display=True, true_time=True):
    videoname = video_path.split('/')[-1]

    # Open video and datastreams
    videoreader = VideoReader(video_path)
    bodyreader = BodyReader(f'{data_path}/keypoints.json', videoname)
    ballreader = BallReader(f'{data_path}/balls.json', videoname)

    # Set output if needed
    if out_path:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        output = cv2.VideoWriter(out_path, fourcc, 20.0, (640, 480))
    
    # Setup trajectories
    ball_trajectory = [{}] * TRAJECTORY_LEN
    body_trajectory = [{}] * TRAJECTORY_LEN
    bounce = False
    ball_dy = 0

    start_time = time.time()

    # Loop over datastreams
    for frame, ball, body in zip(videoreader, ballreader, bodyreader):
        prev_ball = ball_trajectory[-1]
        ball_trajectory.pop(0)
        body_trajectory.pop(0)

        ball_trajectory.append(ball)
        body_trajectory.append(body)

        if ball != {} and prev_ball != {}:
            ball_dy = ball['y'] - prev_ball['y']
            bounce, x = process_ball_trajectory(ball_trajectory)

            # if bounce:
            #     process_bounce(ball_trajectory, body_trajectory)

        # Draw frame
        if display:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = draw_frame(frame, ball, body, ball_dy, bounce)
            cv2.imshow('Are We Still Juggling?', frame)

            if true_time:
                sleep(.032)

        if out_path:
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
    parser.add_argument('--output', type=file_type, required=False,
                        help='Path to the output video.', metavar='FILE')
    parser.add_argument('--display', type=bool, required=False,
                        help='Set output to on or off.')
    parser.add_argument('--truetime', type=bool, required=False, default=False,
                        help='Maximize FPS or use video FPS')
    args = parser.parse_args()

    if not args.display:
        args.truetime = False
    main(args.data, args.video, args.output, args.display, args.truetime)