from retrieve_utils import BodyReader, VideoReader, BallReader

video = VideoReader('data/j.mp4')
balls = BallReader('data/balls.json', 'j.mp4')

def analyse_video(video, balls):
    frames = video.total_frames
    data = balls.data
    print(data)

    ball_presence = 0  
    for key in data:
        if len(data[key]) > 0:
            ball_presence += 1 

    return round((ball_presence / frames) * 100)


print(analyse_video(video, balls))