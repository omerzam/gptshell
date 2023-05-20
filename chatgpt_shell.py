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


def get_command_from_gpt(task, suggestion_count):
    try:
        prompt = f"ubuntu shell {task} show command only show generic parts of the command in brackets: command [arguments]"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=suggestion_count,
            stop=None,
            temperature=0.5,
        )
        response_texts = [choice.text.strip() for choice in response.choices]
        commands = response_texts
        return commands
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
    suggestion_count = int(os.getenv("SUGGESTION_COUNT", 3))

    if task.lower() == "history":
        show_history()
    else:
        commands = get_command_from_gpt(task, suggestion_count)

        if commands:
            if len(commands) == 1:
                command = commands[0]
                print(f"Proposed command: {command}")
            else:
                print("Command suggestions:")
                for i, command in enumerate(commands, start=1):
                    print(f"{i}. {command}")

                selected = int(
                    input("Enter the number of the command you want to execute: "))
                command = commands[selected - 1]
                print(f"Selected command: {command}")

            confirm = input("Do you want to execute this command? (yes/no) ")

            if confirm.lower() in ["yes", "y"]:
                command = process_arguments(command)
                subprocess.run(command, shell=True)
                write_history(command)
            else:
                print("Command not executed.")
        else:
            print("No command found.")
