import json
from jsonschema import validate, ValidationError

def load_and_validate_config(config_path, schema_path):
    """Loads and validates a JSON configuration file against a schema.

    Args:
        config_path (str): Path to the JSON configuration file.
        schema_path (str): Path to the JSON schema file.

    Returns:
        dict: The validated JSON configuration.

    Raises:
        ValidationError: If the configuration is invalid.
        FileNotFoundError: If the config or schema file is not found.
        json.JSONDecodeError: If the config file is not valid JSON.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from {config_path}: {e.msg}", e.doc, e.pos)

    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from {schema_path}: {e.msg}", e.doc, e.pos)

    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        raise ValidationError(f"Configuration validation failed: {e}")

    return config