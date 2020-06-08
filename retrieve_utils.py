import imageio

def get_body_part_bboxes(video_path):
    pass

def get_ball_bboxes(video_path):
    pass

def get_frames(video_path):
    video = imageio.get_reader(video_path)
    no_frames = video.count_frames()

    frames = []

    for i in range(no_frames):
        im = video.get_data(i)
        frames.append(im)
    return frames