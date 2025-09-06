import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_info import schema_get_files_info, schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.function_call import call_function, available_functions
from prompts import system_prompt

def main():
    
    verbose = 0
    if len(sys.argv) == 1:
        print("Usage: python main.py \"Type your prompt\" here")
        sys.exit(1)
    if sys.argv[-1] == "--verbose" or sys.argv[-1] == "-v":
        verbose = 1
        user_prompt = " ".join(sys.argv[1:-1])
    else:
        user_prompt = " ".join(sys.argv[1:])
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    if verbose:
        print(f"User prompt: {user_prompt}")        

    for i in range(20):

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
    

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
