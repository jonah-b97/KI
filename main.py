import argparse
import json
import os
import sys
import time

from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from openai import OpenAI  # pyright: ignore[reportMissingImports]

from call_function import available_functions
from functions.call_function import call_function
from prompts import system_prompt  # pyright: ignore[reportMissingImports]


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("no api key found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
    ]
for _ in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
        )
    if not response.choices:
        time.sleep(2)
        continue

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        if response.usage is not None:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        elif response.usage is None:
            raise RuntimeError("no usage")

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            result_message = call_function(tool_call,args.verbose)
            messages.append(result_message)
            if result_message['content'] is None:
                raise RuntimeError("Error: no content")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
        break
else:
    print("Error: Iteration Limit reached")
    sys.exit(1)
