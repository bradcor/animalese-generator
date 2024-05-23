import subprocess, os, time, wave, threading, requests, socket
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

load_dotenv()
TWITCH_CHANNEL_NAME = os.getenv('TWITCH_CHANNEL_NAME')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
TWITCH_BOT_USERNAME = os.getenv('TWITCH_BOT_USERNAME')
token = None
sock = socket.socket()

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

def read_messages():
    buffer = ""
    while True:
        buffer += sock.recv(1024).decode('utf-8')
        messages = buffer.split("\r\n")
        buffer = messages.pop()

        for message in messages:
            if message.startswith("PING"):
                sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
            else:
                process_message(message)

def extract_display_name(message):
    """Extract display-name from the IRC message."""
    parts = message.split(';')
    for part in parts:
        if part.startswith('display-name='):
            return part.split('=')[1]
    return None

def process_message(message):
    display_name = str(extract_display_name(message)).lower()
    print("Name = " + display_name)
    parts = message.split(' ', 3)
    for part in parts:
        print(part)
    if len(parts) > 3:
        msg_prefix, msg_command, msg_params, msg_text = parts

        if msg_params == 'PRIVMSG':
            print(msg_text)
            user, user_input = msg_text.split(':', 1)
            user_input = str(user_input).strip()
            if display_name == str(TWITCH_CHANNEL_NAME).lower():                
                print(f"Received message: {user_input}")
                call_animalese(user_input)

                # Specify the path to the output audio file
                output_file = "sound.wav"
                duration = get_wav_duration(output_file)
                duration_per_character = duration / (len(user_input) * 1)

                thread = threading.Thread(target=play_output, args=(output_file,))
                thread.start()

                for letter in user_input:
                    print(letter)
                    time.sleep(duration_per_character)

                thread.join()


if __name__ == "__main__":

    token = ACCESS_TOKEN
    # Twitch IRC server details
    server = 'irc.chat.twitch.tv'
    port = 6667

    # Connect to Twitch IRC
    try:
        # Connect to Twitch IRC
        sock.connect((server, port))
        sock.send(f'CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands\n'.encode('utf-8'))
        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {TWITCH_BOT_USERNAME}\n".encode('utf-8'))
        sock.send(f"JOIN #{TWITCH_CHANNEL_NAME}\n".encode('utf-8'))
        print(f"Connected to IRC channel #{TWITCH_CHANNEL_NAME}")
    except Exception as e:
        print(f"Error connecting to IRC: {e}")
        exit(1)


    read_messages()