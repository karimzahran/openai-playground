from pprint import pprint
from openai import OpenAI

client = OpenAI()

# Delete assistants
with open("storage/assistant_id.txt", "r") as assistant_id_file:
    assistant_ids = assistant_id_file.read().splitlines()

for assistant_id in assistant_ids:
    response = client.beta.assistants.delete(assistant_id)
    pprint(response)

with open("storage/assistant_id.txt", "w") as assistant_id_file:
    assistant_id_file.write("")


# Delete files
with open("storage/assistant_file_ids.txt", "r") as assistant_file_ids_file:
    file_ids = assistant_file_ids_file.read().splitlines()

for file_id in file_ids:
    response = client.files.delete(file_id)
    pprint(response)

with open("storage/assistant_files.txt", "w") as assistant_files_file:
    assistant_files_file.write("")

with open("storage/assistant_file_ids.txt", "w") as assistant_file_ids_file:
    assistant_file_ids_file.write("")
