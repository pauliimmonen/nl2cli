import pytest
import json
from unittest.mock import patch
from nl2cli import load_config, save_config, configure, translate_to_command

# Fixture for mocking config file
@pytest.fixture
def mock_config_file(tmp_path):
    config = {
        "os": "Linux",
        "distro": "Ubuntu",
        "api_key": "test_api_key"
    }
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(config, f)
    return str(config_file)

# Test load_config
def test_load_config(mock_config_file):
    with patch('nl2cli.CONFIG_FILE', mock_config_file):
        config = load_config()
        assert config == {
            "os": "Linux",
            "distro": "Ubuntu",
            "api_key": "test_api_key"
        }

def test_load_config_file_not_found():
    with patch('nl2cli.CONFIG_FILE', '/nonexistent/path'):
        config = load_config()
        assert config is None

# Test save_config
def test_save_config(tmp_path):
    config = {"os": "Windows", "api_key": "new_api_key"}
    config_file = tmp_path / "config.json"
    with patch('nl2cli.CONFIG_FILE', str(config_file)):
        save_config(config)
        assert config_file.exists()
        with open(config_file, "r") as f:
            saved_config = json.load(f)
        assert saved_config == config

# Test configure
@pytest.mark.parametrize("inputs,expected", [
    (["1", "test_key"], {"os": "Windows", "distro": "", "api_key": "test_key"}),
    (["2", "test_key"], {"os": "Mac", "distro": "", "api_key": "test_key"}),
    (["3", "Ubuntu", "test_key"], {"os": "Linux", "distro": "Ubuntu", "api_key": "test_key"}),
])
def test_configure_new_config(inputs, expected):
    with patch('builtins.input', side_effect=inputs), \
         patch('nl2cli.save_config') as mock_save, \
         patch('nl2cli.load_config', return_value=None):
        result = configure()
        assert result == expected
        mock_save.assert_called_once_with(expected)

# Test translate_to_command
@patch('nl2cli.OpenAI')
def test_translate_to_command(mock_openai):
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.return_value.choices[0].message.content = "ls -la"
    
    config = {"os": "Linux", "distro": "Ubuntu", "api_key": "test_key"}
    result = translate_to_command("list all files", config)
    
    assert result == "ls -la"
    mock_openai.assert_called_once_with(api_key="test_key")
    mock_client.chat.completions.create.assert_called_once()

# Add more tests as needed