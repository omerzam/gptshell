#!/usr/bin/env python3

import openai
import sys
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_command_from_gpt(task):
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


if __name__ == "__main__":
    task = sys.argv[1]
    command = get_command_from_gpt(task)

    if command:
        print(f"Proposed command: {command}")
        confirm = input("Do you want to execute this command? (yes/no) ")

        if confirm.lower() in ["yes", "y"]:
            subprocess.run(command, shell=True)
        else:
            print("Command not executed.")
    else:
        print("No command found.")
