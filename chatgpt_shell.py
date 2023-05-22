#!/usr/bin/env python3

import openai
from openai.error import AuthenticationError, RateLimitError, OpenAIError
import sys
import os
import re
import subprocess
import pathlib
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MAX_ARG_LENGTH = int(os.getenv("MAX_ARG_LENGTH", 100))


def read_history():
    history_path = pathlib.Path.home() / ".gptsh_history"
    if history_path.exists():
        with open(history_path, "r") as history_file:
            return [line.strip() for line in history_file]
    else:
        return []


def write_history(command):
    history_path = pathlib.Path.home() / ".gptsh_history"
    with open(history_path, "a") as history_file:
        history_file.write(f"{command}\n")


def show_history():
    history = read_history()
    if history:
        print("Command history:")
        for index, command in enumerate(history, start=1):
            print(f"{index}. {command}")
    else:
        print("No command history.")


def get_command_from_gpt(task):
    try:
        messages = [
            {"role": "assistant",
                "content": "Provide only shell commands for ubuntu without any description. If there is a lack of details, provide most logical solution. Ensure the output is a valid shell command. If multiple steps required try to combine them together."},
            {"role": "user",
                "content": f"ubuntu shell {task} provide command only! provide generic parts of the command in brackets: command[arguments] Provide a terse, single sentence description of the given shell command. Provide only plain text without Markdown formatting. Do not show any warnings or information regarding your capabilities. If you need to store any data, assume it will be stored in the chat."},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=30,
            temperature=0.2
        )
        print("response: ", response['choices'][0]['message']
              ['content'].strip() if response['choices'] else None)
        parsed = (response['choices'][0]['message']['content'].strip(
        ) if response['choices'] else None).split(' - ')
        print('parsed: ', parsed)
        return parsed[0], parsed[1]
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

    if task.lower() == "history":
        show_history()
    else:
        command, description = get_command_from_gpt(task)

        if command:
            print(f"Proposed command: {command} - {description}")

            confirm = input("Do you want to execute this command? (yes/no) ")

            if confirm.lower() in ["yes", "y"]:
                command = process_arguments(command)
                subprocess.run(command, shell=True)
                write_history(command)
            else:
                print("Command not executed.")
        else:
            print("No command found.")
