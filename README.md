# nl2cli: Natural Language to Command-Line Translator

nl2cli is an innovative Python-based tool that seamlessly converts natural language instructions into precise command-line commands across various operating systems. Leveraging OpenAI's powerful GPT-3.5-turbo model, nl2cli delivers accurate and efficient command-line equivalents for user inputs.

## Quick Start Guide

1. Clone this repository or download the `nl2cli.py` file.
2. Install the required OpenAI library:

   ```
   pip install openai
   ```

3. Ensure you have a OpenAI API key.

## Initial Setup

Before your first use of nl2cli, you'll need to configure it with your operating system details and API key. The configuration process will automatically initiate on the first run, but you can also manually trigger it with:

```
python nl2cli.py --configure
```

Follow the given instructions.

## How to Use

Transform natural language into command-line instructions with this straightforward syntax:

```
python nl2cli.py "your natural language instruction"
```

### Practical Examples

1. Creating a new directory:
   ```
   python nl2cli.py "create a new folder named projects"
   Output: mkdir projects
   ```

2. Locating Python files:
   ```
   python nl2cli.py "find all python files in the current directory and its subdirectories"
   Output: find . -type f -name "*.py"
   ```

3. Modifying Git configuration:
   ```
   python nl2cli.py "change default git editor to vim"
   Output: git config --global core.editor "vim"
   ```

nl2cli will generate the appropriate command-line instruction tailored to your specified operating system.

## Important Notes

- Translation accuracy is contingent on the OpenAI model and the clarity of your natural language input.
- Always review generated commands before execution, especially for system-critical operations.
- nl2cli currently utilizes the GPT-3.5-turbo model. Stay informed about potential updates for newer models.

## Troubleshooting Tips

If you encounter any issues:
1. Verify that your OpenAI API key is valid and has sufficient credits.
2. Ensure the `config.json` file exists and contains accurate information.
3. For reconfiguration, use the `--configure` flag as outlined in the Initial Setup section.

## Responsible Usage

Remember to use nl2cli responsibly and always verify the generated commands before execution. 
