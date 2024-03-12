import json
import os

# Load the rasa endpoint
def load_rasa_endpoint(config_file_path, use_local=True):
    try:
        # Check if the config file exists
        if not os.path.isfile(config_file_path):
            raise FileNotFoundError(f"Config file '{config_file_path}' not found.")

        with open(config_file_path, encoding="utf-8") as config_file:
            config_data = json.load(config_file)

        if use_local:
            rasa_endpoint = config_data.get('url_local')
        else:
            rasa_endpoint = config_data.get('url_aws')

        # Check if the required keys are present in the config file
        if not rasa_endpoint:
            raise KeyError(f"Required key ('url_local' or 'url_aws') not found in the config file.")

        return rasa_endpoint

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        # Raise an exception or handle the error in another way
        raise ValueError("Invalid configuration file or missing required keys.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        # Raise an exception or handle the error in another way
        raise