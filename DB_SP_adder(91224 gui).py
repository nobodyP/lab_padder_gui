import os
import ffmpeg
import tkinter
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import ttk

#################################################################################### --- setting up interface

root = tkinter.Tk()
root.title("menKissing")
root.geometry("400x200+0+0")
root.resizable(False, False)

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# start condition, when you press start button this turns true and lets the program finish
start = tkinter.BooleanVar(value=False)

# background =)
bg = PhotoImage(file = (f"{script_dir}\\_assets\\bg.png"))
missing = PhotoImage(file = (f"{script_dir}\\_assets\\missing.png"))

canvas1 = tkinter.Canvas(root, width = 400, height = 400)
canvas1.pack(fill = "both", expand = True)
canvas1.create_image(0, 0, image = bg, anchor = "nw")
canvas1.create_image(400, 0, image = missing, anchor = "ne") 

def disable():
    pass
root.protocol('WM_DELETE_WINDOW', disable)

def egress():
    os._exit(0)

def askfor_inp():
    global input_folder
    input_folder = filedialog.askdirectory(initialdir="/", title="Select input directory")

def askfor_out():
    global output_folder
    output_folder = filedialog.askdirectory(initialdir="/", title="Select output directory")


start_button = ttk.Button(root, text="Start Program", width=20, command=lambda: start.set(True))
exit_button = ttk.Button(root, text="Exit", command=lambda: egress())
inp_button = ttk.Button(root, text="select input dir", command=lambda: askfor_inp())
out_button = ttk.Button(root, text="select output dir", command=lambda: askfor_out())


start_button.place(x=20, y=20)
exit_button.place(x=150, y=20)
inp_button.place(x=20, y=60)
out_button.place(x=150, y=60)

root.wait_variable(start)

####################################################################################



blank_file = os.path.join(script_dir, "blank.wav")

# Create a blank .wav file with a duration of 0.5 seconds and matching original audio format
def create_blank_file(reference_file, output_file):
    probe = ffmpeg.probe(reference_file)
    audio_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'audio')
    
    sample_rate = audio_stream['sample_rate']
    channels = audio_stream['channels']
    ffmpeg.input('anullsrc=channel_layout=stereo:sample_rate={}'.format(sample_rate), f='lavfi').output(output_file, t=0.5, acodec='pcm_s16le', ac=channels).run(overwrite_output=True)

# Get all .wav files in input folder
files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]

for file in files:
    input_file = os.path.join(input_folder, file)
    output_file = os.path.join(output_folder, file)

    # Create a blank file with the same sample rate and number of channels as the input file
    create_blank_file(input_file, blank_file)

    # Create a temporary list file for ffmpeg concat
    concat_list_file = os.path.join(script_dir, 'concat_list.txt')
    with open(concat_list_file, 'w') as f:
        # Add silence (start), the original file, and silence (end)
        f.write(f"file '{blank_file}'\n")  # Silence at the beginning
        f.write(f"file '{input_file}'\n")  # Original audio file
        f.write(f"file '{blank_file}'\n")  # Silence at the end
    
    # Run ffmpeg using the concat list
    try:
        ffmpeg.input(concat_list_file, f='concat', safe=0).output(output_file, acodec='copy').run(overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"Error while processing file {file}: {e.stderr.decode('utf8')}")

# Clean up concat_list.txt after processing
if os.path.exists(concat_list_file):
    os.remove(concat_list_file)

# Run the additional script with relative paths
print("Now for the labels...")

os.system(f"python {script_dir}\lab_padder.py -d {input_folder} -o {output_folder}")

print("Done!")