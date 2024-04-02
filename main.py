import subprocess
from pydub import AudioSegment
from pydub.playback import play
import os

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
                        # ,stdout=subprocess.DEVNULL,
                        # stderr=subprocess.STDOUT
                        )
    except Exception as e:
        print(f"An error occurred while playing the file: {e}")

if __name__ == "__main__":

    user_input = input("Please enter the string for animalese: ")
    call_animalese(user_input)

    while (user_input != "quit"):
        # Specify the path to the output audio file
        output_file = "sound.wav"
        play_output(output_file)

        user_input = input("Please enter the string for animalese: ")
        call_animalese(user_input)
