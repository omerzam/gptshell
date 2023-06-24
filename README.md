# GPTShell

GPTShell is an interactive shell command suggestion tool powered by OpenAI's GPT-3 model. It takes in the description of a task as an input and provides shell command suggestions to accomplish the task. It is designed to streamline the process of working in a shell environment, making it more user-friendly and efficient.

## Features

- **Command Suggestions**: GPTShell leverages the power of GPT-3 to generate accurate and practical command suggestions based on the user's input.
- **Interactive Input**: The tool prompts users to fill in any required arguments for the suggested commands.
- **Command Execution**: Users can directly execute the selected command within the script.
- **Command History**: GPTShell keeps track of the commands executed by the user for easy reference.
- **Customizable Settings**: Users can customize the number of command suggestions and the maximum argument length via environment variables.

## Setup

### Requirements

- Python 3.10
- OpenAI Python package
- A valid OpenAI API key

### Installation

1. Clone this repository to your local machine:
```
git clone https://github.com/omerzam/gptshell
```

2. Move into the project directory:

```
cd gptshell
```


3. Set up a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

4. Install the required packages:

```
pip install -r requirements.txt
```

5. Set your OpenAI API key as an environment variable:

```
export OPENAI_API_KEY='your-key-here'
```

## Usage

To use GPTShell, run the `chatgpt_shell.py` script and provide a task description as a command-line argument:

```
python chatgpt_shell.py "create a new directory"
```

The tool will display command suggestions and explanations for the task. If you wish to execute a command, enter its number and confirm execution.

## Configuration

GPTShell allows customization through the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key. This is required to interact with the OpenAI API.
- `MAX_ARG_LENGTH`: The maximum length for arguments in a command. Default is 100.
- `SUGGESTION_COUNT`: The number of command suggestions to display. Default is 3.

## Contributing

We welcome contributions! Feel free to submit a pull request or open an issue.

## License

GPTShell is licensed under the MIT License.

## Disclaimer

Please note that GPTShell interacts with OpenAI's GPT-3 model, which may incur costs depending on the usage. Always monitor your OpenAI API usage while using this tool.

## Contact

For any issues or suggestions, please reach out through the project's issue tracker on GitHub.
