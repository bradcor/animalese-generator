# Animalese Audio Generator

## General info
This project allows you to generate audio from text in the style of animalese from the Animal Crossing games.
This has been updated to read from messages from Twitch, specifically if the broadcaster typed the message.
The project will send data to Vtube Studio as variables for rigging and animating of model based on posted text and is synced up with audio playback.

## Usage

```
$ py main.py
```

Make sure you have your .env file updated with the following lines:
- TWITCH_CHANNEL_NAME='Channel's Chat To Connect To'
- TWITCH_BOT_USERNAME='All Lowercase Name of Bot Maker (name of account you used to get access token)'
- ACCESS_TOKEN = 'oauth: Access token from [Twitch token generator](https://twitchtokengenerator.com/)'

Make sure to have ACCESS_TOKEN lead with oauth:
An example of this would be: oauth:RandomAccessCode
```

## Technologies
Project is created with:
* pydub

## Installing required dependencies
```
$ pip install pydub

## Pending Implementation
- Websocket connection to VTS
- Parameter generation in VTS
- Parameter passing in VTS

