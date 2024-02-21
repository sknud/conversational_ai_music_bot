import json

# Load the rasa endpoint
def load_rasa_endpoint(config_file_path, use_local=True):
    try:
        with open(config_file_path, encoding="utf-8") as config_file:
            config_data = json.load(config_file)
        if use_local:
            rasa_endpoint = config_data['url_local']
        else:
            rasa_endpoint = config_data['url_aws']
        return rasa_endpoint
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None