#!/usr/bin/env python3

import openai
from openai.error import AuthenticationError, RateLimitError, OpenAIError
import sys
import os
import re
import subprocess
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MAX_ARG_LENGTH = int(os.getenv("MAX_ARG_LENGTH", 100))


def get_command_from_gpt(task):
    try:
        prompt = f"ubuntu shell {task} show command only: command [arguments]"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response_text = response.choices[0].text.strip()
        command = response_text
        return command
    except AuthenticationError:
        print("Error: Invalid OpenAI API key.")
        return None
    except RateLimitError:
        print("Error: API rate limit exceeded. Please try again later.")
        return None
    except OpenAIError as e:
        print(f"Error: OpenAI API error - {e}")
        return None
    except Exception as e:
        print(f"Error: Unexpected error occurred - {e}")
        return None


def global_validation(value):
    if len(value) > MAX_ARG_LENGTH:
        raise ValueError(
            f"Provided value exceeds the maximum allowed length of {MAX_ARG_LENGTH} characters.")
    return value


def process_arguments(command):
    argument_pattern = re.compile(r'\[([^\]]+)\]')
    matches = argument_pattern.findall(command)
    for match in matches:
        value = input(f"Please enter a value for {match}: ")
        value = global_validation(value)
        command = command.replace(f"[{match}]", value)
    return command


if __name__ == "__main__":
    task = " ".join(sys.argv[1:])
    command = get_command_from_gpt(task)

    if command:
        print(f"Proposed command: {command}")
        confirm = input("Do you want to execute this command? (yes/no) ")

        if confirm.lower() in ["yes", "y"]:
            try:
                command = process_arguments(command)
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

            subprocess.run(command, shell=True)
        else:
            print("Command not executed.")
    else:
        print("No command found.")
