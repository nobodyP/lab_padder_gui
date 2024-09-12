import os
import ffmpeg

input_folder = '/Lab_and_Wav/'
output_folder = '/Output/'
    
blank_file = "blank.wav"

# Create a blank .wav file with a duration of 5 seconds
ffmpeg.input('anullsrc=channel_layout=stereo:sample_rate=44100').output(blank_file, t=0.5).run()

start_audio_file = "blank.wav"

# Get all .wav files in input folder
files = [f for f in os.li   stdir(input_folder) if f.endswith('.wav')]

for file in files:
    input_file = os.path.join(input_folder, file)
    output_file = os.path.join(output_folder, file)
    
    stream = ffmpeg.input(start_audio_file).output(input_file, file, map='0:a', map_metadata=1).run(overwrite_output=True)

os.system("python lab_padder.py -d input_folder -o output_folder")  