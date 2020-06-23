from moviepy.editor import *
import IPython
import essentia
import essentia.standard as es
from essentia.standard import *
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt

video = VideoFileClip("data/j.mp4")
audio = video.audio
audio.write_audiofile("test.wav")

IPython.display.Audio("test.wav")

# Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame features
features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                              rhythmStats=['mean', 'stdev'],
                                              tonalStats=['mean', 'stdev'])('test.wav')

# Loading audio file
audio = MonoLoader(filename='test.wav')()

# Compute beat positions and BPM
rhythm_extractor = RhythmExtractor2013(method="multifeature")
bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

print("BPM:", bpm)
print("Beat positions (sec.):", beats)
print("Beat estimation confidence:", beats_confidence)

# Mark beat positions on the audio and write it to a file
# Let's use beeps instead of white noise to mark them, as it's more distinctive
marker = AudioOnsetsMarker(onsets=beats, type='beep')
marked_audio = marker(audio)
MonoWriter(filename='test.wav')(marked_audio)

%matplotlib inline
plt.rcParams['figure.figsize'] = (15, 6) # set plot sizes to something larger than default

plot(audio)
for beat in beats:
    plt.axvline(x=beat*44100, color='red')

plt.title("Audio waveform and the estimated beat positions")
