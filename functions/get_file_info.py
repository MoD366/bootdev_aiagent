import os
from config import MAX_CHARS
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    if not in_working_directory(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    output = "Result for "

    if directory == ".":
        output += "current directory:\n"
    else:
        output += f"'{directory}' directory:\n"

    entries = []
    try:
        for entry in os.listdir(full_path):
            entries.append(f" - {entry}: file_size={os.path.getsize(f"{full_path}/{entry}")}, is_dir={os.path.isdir(f"{full_path}/{entry}")}")
    except Exception as e:
        print(e)
    output += "\n".join(entries)

    return output
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def in_working_directory(working_directory,path):
    if os.path.abspath(os.path.join(working_directory, path)).startswith(os.path.abspath(f"./{working_directory}")):
        return True
    return False

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    if not in_working_directory(working_directory,file_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    print(full_path)

    with open(full_path, "r") as file:
        content_string = file.read(MAX_CHARS)
        if len(content_string) == MAX_CHARS:
            content_string += f'[...File "{file_path}" truncated at 10000 characters]'
        return content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file from which to get the content, relative to the working directory.",
            ),
        },
    ),
)