import argparse
from classes.assistants import Assistant
from classes.audio import Audio, Voice


def main(use_audio: bool):
    instructions = ""
    audio = Audio(Voice.ALLOY)
    assistant = Assistant(instructions=instructions, audio=audio)

    quit_instruction = "Say 'exit' to quit" if use_audio else "Type 'exit' to quit"
    print(f"\nWelcome to your personal AI Assistant. {quit_instruction}.\n")

    while True:
        if use_audio:
            input("Press Enter to start recording...")
            # Can you figure out how to record audio and then transcribe it to user_input?
            # Hint: You'll need to save the recording as a .wav file in the media folder.
        else:
            user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        assistant.send_message(user_input, return_audio=use_audio)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the personal AI Assistant")
    parser.add_argument("--audio", action="store_true", help="Chat using audio")
    args = parser.parse_args()

    main(use_audio=args.audio)
