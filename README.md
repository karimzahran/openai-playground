# Welcome to the OpenAI Playground!

Hey there, high schoolers! If you're curious about coding, AI, or just want to create something cool, you've come to the right place. This project is all about building your very own AI Assistant using Python and OpenAI's powerful tools. Don't worry if you're new to coding; we'll walk you through everything step by step.

## What's Inside the Code

- **main.py**: This is where the magic starts. It's the main script that you'll run to interact with your AI Assistant. You can chat using text or voice, thanks to the code here.
- **classes/**: This directory contains several Python files, each defining a specific part of our project:
  - **assistants.py**: Manages interactions with the OpenAI Assistant.
  - **audio.py**: Handles all audio operations, like recording your voice or playing the assistant's responses.
  - **images.py**: Allows creating images from text prompts using OpenAI's DALL-E model.
- **cleanup.py**: A script to clean up any data created by the project, like deleting created assistants or files.
- **files/**: A directory for storing files that your AI Assistant can use for knowledge retrieval.

## Setting Up the Project in VS Code

1. **Install Python**: Make sure you have Python installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

2. **Get VS Code**: If you don't already have it, download and install Visual Studio Code (VS Code) from [code.visualstudio.com](https://code.visualstudio.com/).

3. **Open the Project**: Open VS Code, go to `File > Open Folder`, and select the folder where you've saved this project.

4. **Set Up a Virtual Environment**:

   - Open the terminal in VS Code by going to `Terminal > New Terminal`.
   - Create a virtual environment by running:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows, run:
       ```bash
       .\venv\Scripts\activate
       ```
     - On macOS and Linux, run:
       ```bash
       source venv/bin/activate
       ```

5. **Install Dependencies**:
   - With your virtual environment activated, install the project's dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

## Running the Project

With everything set up, you're now ready to bring your AI Assistant to life! Ensure your virtual environment is activated in the terminal, then proceed with the following steps:

1. **Run the Main Script**: To start interacting with your AI Assistant, execute the main script by running:

   ```bash
   python main.py
   ```

   Optionally, you can enable voice interaction by adding the `--audio` flag:

   ```bash
   python main.py --audio
   ```

2. **Cleanup**: After you're done experimenting with your AI Assistant, you might want to clean up any data or files created during the process. Run the cleanup script by executing:
   ```bash
   python cleanup.py
   ```

Enjoy exploring the capabilities of your personal AI Assistant!
