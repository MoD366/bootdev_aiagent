import os
from google import genai
from google.genai import types
from functions.get_file_info import in_working_directory

def write_file(working_directory, file_path, content):
    if not in_working_directory(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    full_path = os.path.join(working_directory, file_path)
    full_dir = "/".join(full_path.split("/")[:-1])
    
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)

    with open(full_path, "w") as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content into a file and creates it if it doesn't exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write into, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            ),
        },
    ),
)