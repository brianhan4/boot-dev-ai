import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions
from prompts import system_prompt
import sys

VERBOSE_FLAG = "--verbose"
def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print('Correct usage: python main.py "your prompt"')
        sys.exit(1)

    is_verbose = VERBOSE_FLAG in args


    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, args, user_prompt)


def generate_content(client, messages, args, user_prompt):


    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt)
        )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if VERBOSE_FLAG in args:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        
    
    function_calls = response.function_calls
    if not function_calls:
        return response.text
        
    for function_call_part in function_calls:
        print (f"Calling function: {function_call_part.name}({function_call_part.args})")
    


if __name__ == "__main__":
    main()

