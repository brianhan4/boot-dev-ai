import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions, call_function
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
    is_verbose = VERBOSE_FLAG in args


    for i in range(20):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt)
            )
            for candidate in (response.candidates or []):
                messages.append(candidate.content)

            function_responses = []
            for function_call_part in (response.function_calls or []):
                if is_verbose:
                    print(f"- Calling function: {function_call_part.name}")
                function_call_result = call_function(function_call_part, is_verbose)

                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")

                if is_verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])

            if function_responses:
                tool_msg = types.Content(
                    role="user",
                    parts=function_responses,
                )
                messages.append(tool_msg)
                continue
            
            elif response.text:
                print("Final response:")
                print(response.text)
                break

        except Exception as e:
            if is_verbose:
                print(f"Error: {e}")




        


if __name__ == "__main__":
    main()

