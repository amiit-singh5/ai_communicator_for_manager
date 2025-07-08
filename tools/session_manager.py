import requests
from  tools.config_reader import ConfigurationReader

class SessionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.session = None
        self.base_url = None
        self.headers = None
        self.json_message = None
        self.config = ConfigurationReader().get_logging_config()

    def __enter__(self):
        self.session = requests.Session()
        return self

    def configure(self, base_url, headers, json_message):
        self.base_url = base_url
        self.headers = headers
        self.json_message = json_message

    def get(self, endpoint, **kwargs):
        url = self._full_url(endpoint)
        return self.session.get(url, **kwargs)

    def post(self, endpoint="", data=None, json=None, **kwargs):
        url = endpoint or self.base_url
        return self.session.post(url, data=data, json=json or self.json_message, headers=self.headers, **kwargs)

    # def post(self, endpoint, data=None, json=None, **kwargs):
    #     url = self._full_url(endpoint)
    #     return self.session.post(url, data=data, json=json, **kwargs)

    def _full_url(self, endpoint):
        if not self.base_url:
            raise ValueError("Base URL not configured")
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
        SessionManager._instance = None
