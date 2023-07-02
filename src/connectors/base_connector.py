from configparser import ConfigParser
from typing import List

from src.utils.constants import CONNECTOR_CONFIG_PATH

config_parser = ConfigParser()
config_parser.read_file(open(CONNECTOR_CONFIG_PATH))


class BaseConnector:
    active: bool = False

    def __init__(self, **kwargs):
        try:
            self.active = kwargs["active"] == "true"
        except KeyError as e:
            raise ValueError("Missing required argument") from e

    def auth(self):
        """Run authentication process for the connector if needed"""
        raise NotImplementedError()

    def get_unread_messages_inbox(self) -> List[str]:
        """Get unread messages from the inbox"""
        raise NotImplementedError
