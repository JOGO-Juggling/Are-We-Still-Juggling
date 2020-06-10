from retrieve_utils import BodyReader, VideoReader, BallReader
from draw_utils import draw_frame
import cv2

from time import sleep

def main(video):
    videoreader = VideoReader(f'data/videos/{video}')
    bodyreader = BodyReader('data/keypoints.json', video)
    ballreader = BallReader('data/balls.json', video)
    
    output = cv2.VideoWriter('output.mp4', -1, 20.0, (640,480))

    for frame, ball, body in zip(videoreader, ballreader, bodyreader):
        frame = draw_frame(frame, ball, body)
        cv2.imshow('Are We Still Juggling?', frame)
        output.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(0.016)

    output.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main('0f272d8bfd2947a0b37f0deaf2fe20bd.MOV')