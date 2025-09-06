from google import genai
from google.genai import types
from functions.get_file_info import schema_get_files_info, schema_get_file_content, get_files_info, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from config import WORKING_DIRECTORY


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_dictionary = {"get_files_info": get_files_info, "get_file_content": get_file_content, "run_python_file": run_python_file, "write_file": write_file}

    function_args = function_call_part.args.copy()
    function_args["working_directory"] = WORKING_DIRECTORY
    try:
        function_result = function_dictionary[function_call_part.name](**function_args)
    except Exception as e:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
)

available_functions = types.Tool(
       function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )