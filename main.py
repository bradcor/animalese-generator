import subprocess
from pydub import AudioSegment
from pydub.playback import play
import os
import time
import wave
import threading

def call_animalese(input_text):
    # Assuming animalese.py is in the same directory and ready to receive input from stdin
    process = subprocess.Popen(['python', 'animalese.py'], stdin=subprocess.PIPE, text=True)
    process.communicate(input_text)

def play_output(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Cannot find the audio file: {file_path}")
        return

    # Play the output audio file
    try:
        subprocess.call(['ffplay', '-nodisp', '-autoexit', file_path]
                         ,stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT
                        )
    except Exception as e:
        print(f"An error occurred while playing the file: {e}")

def get_wav_duration(wav_path):
    with wave.open(wav_path, 'r') as wav_file:
        # Get the total number of frames in the file
        frames = wav_file.getnframes()
        
        # Get the frame rate (number of frames per second)
        frame_rate = wav_file.getframerate()
        
        # Calculate the duration in seconds
        duration_seconds = frames / float(frame_rate)
        
        return duration_seconds
    
def send_sound(sound):
    print(sound)

if __name__ == "__main__":

    user_input = input("Please enter the string for animalese: ")
    
    user_input = "Start"

    while (user_input != "quit"):

        user_input = input("Please enter the string for animalese: ")
        call_animalese(user_input)

        # Specify the path to the output audio file
        output_file = "sound.wav"
        duration = get_wav_duration(output_file)
        duration_per_character = duration / len(user_input)

        thread = threading.Thread(target=play_output, args=(output_file,))
        thread.start()        

        # threading adds 120 ms delay to audio play
        # time.sleep(0.12)
        for letter in user_input:
            print(letter)
            time.sleep(duration_per_character)

        thread.join()
