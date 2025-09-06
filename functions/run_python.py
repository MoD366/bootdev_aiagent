import os
import subprocess
from google import genai
from google.genai import types
from functions.get_file_info import in_working_directory

def run_python_file(working_directory, file_path, args=[]):
    if not in_working_directory(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.join(working_directory,file_path)):
        return f'Error: File "{file_path}" not found.'
    if file_path.split(".")[-1] != "py":
        return f'Error: "{file_path}" is not a Python file.'
    try:        
        completed_process = subprocess.run(["python3",os.path.join(working_directory,file_path)] + args, stdout=True, stderr=True, timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if completed_process.stdout == "" and completed_process.stderr == "":
        return "No output produced."
    output = f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
    if completed_process.returncode != 0:
        output += f"Process exited with code {completed_process.returncode}"
    return output

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python3 script, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python3 script file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of the arguments to call the Python3 script with. If not provided, the script will run without any arguments.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)