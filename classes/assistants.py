import os
from typing import NoReturn
from typing_extensions import override
from openai import OpenAI, AssistantEventHandler
from openai.types.beta import Assistant
from .audio import Audio


class Assistant:
    """
    A class to manage interactions with an OpenAI Assistant, including uploading files
    to enable knowledge retrieval.
    """

    def __init__(self, instructions: str, audio: Audio):
        """
        Initializes the Assistant class with instructions and an audio object.

        :param instructions: Instructions for the assistant.
        :param audio: An Audio object for handling audio operations.
        """
        self.client = OpenAI()
        self.assistant = self.retrieve_assistant(instructions)
        self.thread = self.client.beta.threads.create()
        self.audio = audio
        self.check_and_create_assistant_files()

    def save_assistant_id(self, assistant_id: str) -> None:
        """
        Saves the assistant ID to a file.

        :param assistant_id: The ID of the assistant to be saved.
        """
        with open("storage/assistant_id.txt", "w") as file:
            file.write(assistant_id)

    def retrieve_assistant(self, instructions: str) -> Assistant:
        """
        Retrieves an assistant by ID, or creates a new one if no ID is found.

        :param instructions: Instructions for creating a new assistant if necessary.
        :return: An Assistant object.
        """
        assistant_id = ""
        with open("storage/assistant_id.txt", "r") as file:
            assistant_id = file.read().strip()
        if assistant_id:
            return self.client.beta.assistants.retrieve(assistant_id)
        else:
            assistant_name = input("\nPlease enter a name for your new assistant: ")
            assistant = self.client.beta.assistants.create(
                model="gpt-3.5-turbo",
                name=assistant_name,
                instructions=instructions,
                tools=[{"type": "retrieval"}],
            )
            self.save_assistant_id(assistant.id)
            return assistant

    def create_assistant_file(self, file_path: str) -> str:
        """
        Creates an assistant file from a given file path.

        :param file_path: The path to the file to be uploaded.
        :return: The ID of the created file.
        """
        file = self.client.files.create(
            file=open(file_path, "rb"), purpose="assistants"
        )
        self.client.beta.assistants.files.create(
            assistant_id=self.assistant.id, file_id=file.id
        )
        return file.id

    def check_and_create_assistant_files(self) -> None:
        """
        Checks for new files in the 'files' directory and uploads them as assistant files.
        """
        existing_files = set()
        with open("storage/assistant_files.txt", "r") as file:
            existing_files = set(file.read().splitlines())

        directory_files = set(os.listdir("files"))
        unsupported_files = {".DS_Store"}
        new_files = directory_files - existing_files - unsupported_files

        file_ids = []
        for file_name in new_files:
            file_ids.append(
                self.create_assistant_file(os.path.join("files", file_name))
            )

        with open("storage/assistant_files.txt", "a") as file:
            for file_name in new_files:
                file.write(file_name + "\n")

        with open("storage/assistant_file_ids.txt", "w") as file:
            for file_id in file_ids:
                file.write(file_id + "\n")

    def create_message(self, content: str) -> None:
        """
        Creates a message in the assistant's thread.

        :param content: The content of the message to be created.
        """
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=content
        )

    def stream_run(self, return_audio: bool) -> NoReturn:
        """
        Streams the run of the assistant, optionally returning audio.

        :param return_audio: Whether to return audio or not.
        """
        with self.client.beta.threads.runs.create_and_stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            event_handler=EventHandler(audio=self.audio, return_audio=return_audio),
        ) as stream:
            stream.until_done()

    def send_message(self, content: str, return_audio: bool = False) -> None:
        """
        Sends a message to the assistant and handles the response.

        :param content: The content of the message to send.
        :param return_audio: Whether the response should be in audio.
        """
        self.create_message(content)
        self.stream_run(return_audio=return_audio)


class EventHandler(AssistantEventHandler):
    def __init__(self, audio: Audio, return_audio: bool):
        super().__init__()
        self.audio = audio
        self.return_audio = return_audio
        self.response = ""

    @override
    def on_text_created(self, text) -> None:
        if not self.return_audio:
            print("Assistant: ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot) -> None:
        if self.return_audio:
            self.response += delta.value
        else:
            print(delta.value, end="", flush=True)

    @override
    def on_end(self) -> None:
        if self.return_audio and self.response.strip():
            output_file = self.audio.create_speech(
                input=self.response,
                output_file="media/speech_output.mp3",
            )
            self.audio.play_audio(file=output_file)
            self.response = ""
        else:
            print("\n")
