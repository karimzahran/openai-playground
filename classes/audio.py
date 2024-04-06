from enum import Enum
from openai import OpenAI
import os
import queue

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import warnings
import threading
import numpy as np
import sounddevice as sd
import wavio

warnings.filterwarnings(action="ignore", category=DeprecationWarning)


class Voice(Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


class Audio:
    """
    A class to handle audio operations including creating speech from text,
    transcribing audio, playing audio files, and recording audio.
    """

    def __init__(self, voice: Voice):
        """
        Initializes the Audio class with a specific voice.

        :param voice: An instance of the Voice Enum representing the voice to be used.
        """
        self.client = OpenAI()
        self.voice = voice.value
        pygame.mixer.init()

    def create_speech(self, input: str, output_file: str) -> str:
        """
        Creates speech from text and saves it to a file.

        :param input: The text to be converted to speech.
        :param output_file: The path to the file where the speech will be saved.
        :return: The path to the output file.
        """
        response = self.client.audio.speech.create(
            model="tts-1", input=input, voice=self.voice
        )
        response.stream_to_file(file=output_file)
        return output_file

    def create_transcription(self, file: str) -> str:
        """
        Creates a transcription of an audio file.

        :param file: The path to the audio file to be transcribed.
        :return: The transcription text.
        """
        audio_file = open(file, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
        return transcript.text

    def create_translation(self, file: str) -> str:
        """
        Translates an audio file into English.

        :param file: The path to the audio file to be translated.
        :return: The translation text.
        """
        audio_file = open(file, "rb")
        translation = self.client.audio.translations.create(
            model="whisper-1", file=audio_file
        )
        return translation.text

    def play_audio(self, file: str) -> None:
        """
        Plays an audio file.

        :param file: The path to the audio file to be played.
        """
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1000)

    def record_audio(self, file: str) -> str:
        """
        Records audio from the default microphone until the Enter key is pressed.

        :param file: The path to the file where the recording will be saved.
        :return: The path to the recorded audio file.
        """
        q = queue.Queue()

        def callback(indata, frames, time, status):
            """Callback function for the audio stream."""
            q.put(indata.copy())

        def stop_recording():
            """Stops the recording when the Enter key is pressed."""
            input()
            event.set()
            print("Recording stopped. Generating response...\n")

        event = threading.Event()
        threading.Thread(target=stop_recording).start()

        frames = []
        sample_rate = 44100
        with sd.InputStream(callback=callback, samplerate=sample_rate, channels=1):
            print("Recording... (press Enter to stop)")
            while not event.is_set():
                try:
                    data = q.get()
                    frames.append(data)
                except queue.Empty:
                    pass

        recording = np.concatenate(frames, axis=0)
        wavio.write(file, recording, sample_rate, sampwidth=2)

        return file
