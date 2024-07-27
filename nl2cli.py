import sys
import json
import os
from openai import OpenAI
from openai.types.chat import ChatCompletion

CONFIG_FILE = os.path.expanduser("./config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        print(f"Config file not found at: {CONFIG_FILE}")
    return None

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def configure():
    print("Welcome to the NL to CLI translator configuration!")
    existing_config = load_config()

    while True:
        print("Please select your operating system:")
        print("1. Windows")
        print("2. Mac")
        print("3. Linux")
        print("Empty keep current config")
        os_choice = input("Enter the number of your choice (1-3): ").strip()
        if os_choice in ['', '1', '2', '3']:
            if os_choice == "":
                if existing_config and 'os' in existing_config:
                    selected_os = existing_config['os']
                    break
                else:
                    print("Existing config not found")
                    continue
            os_map = {'1': 'Windows', '2': 'Mac', '3': 'Linux'}
            selected_os = os_map[os_choice]
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    if selected_os == 'Linux':
        if existing_config and 'distro' in existing_config:
            distro = input(f"Please enter your Linux distribution (e.g., Ubuntu, Fedora, Arch) [Current: {existing_config['distro']}]: ").strip()
            if distro == "":
                distro = existing_config['distro']
        else:
            distro = input("Please enter your Linux distribution (e.g., Ubuntu, Fedora, Arch): ").strip()
    else:
        distro = ""
    
    if existing_config and 'api_key' in existing_config:
        api_key = input(f"Please enter your OpenAI API key [Current: {existing_config['api_key']}]: ").strip()
        if api_key == "":
            api_key = existing_config['api_key']
    else:
        api_key = input("Please enter your OpenAI API key: ").strip()

    config = {"os": selected_os, "distro": distro, "api_key": api_key}
    save_config(config)
    print(f"Configuration saved at {CONFIG_FILE}")
    print(f"Using {distro + ' ' if distro else ''}{selected_os} as the target operating system.")
    return config

def translate_to_command(natural_language, config):
    try:
        client = OpenAI(api_key=config["api_key"])
        selected_os = config.get("os", "Unknown")
        distro = config.get("distro")
        system_content = f"You are a helpful assistant that translates natural language instructions into command-line commands for {distro + ' ' if distro else ''}{selected_os}. Provide only the command as plain string without any formatting and any explanation."

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": natural_language
                }
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    config = load_config()
    if config is None or "api_key" not in config or "os" not in config:
        config = configure()

    if len(sys.argv) < 2:
        print("Usage: python nl2cli.py 'your natural language instruction'")
        print("To reconfigure, use: python nl2cli.py --config")
        sys.exit(1)

    if sys.argv[1] == "--config":
        configure()
        sys.exit(0)

    natural_language = ' '.join(sys.argv[1:])
    command = translate_to_command(natural_language, config)
    print(command)

if __name__ == "__main__":
    main()