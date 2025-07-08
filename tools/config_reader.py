import json
import os


class ConfigurationReader:
    def __init__(self, config_path="tools/config.json"):
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self):
        # if not os.path.exists(self.config_path):
        #     raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get_logging_config(self):
        return self.config_data.get('logging', {})

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def get_openroute_config(self):
        return self.config_data.get('other_config')
    
    def get_headers(self):
        return self.config_data.get("other_config", {}).get('headers')

    def get_json_message(self):
        return self.config_data.get("other_config", {}).get('payload')

    def get_url(self):
        return self.config_data.get("other_config", {}).get("url")


# print(ConfigurationReader().get_logging_config())
# print(ConfigurationReader().get_openroute_config())


