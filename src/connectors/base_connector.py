from configparser import ConfigParser
from typing import Iterable

from ..utils.constants import CONNECTOR_CONFIG_PATH
from ..utils.models import Message

config_parser = ConfigParser()
config_parser.read_file(open(CONNECTOR_CONFIG_PATH))


class BaseConnector:
    name: str
    active: bool = False

    def __init__(self, name: str, active: str, **kwargs):
        try:
            self.active = active == "true"
            self.name = name
        except KeyError as e:
            raise ValueError("Missing required argument") from e

    def auth(self):
        """Run authentication process for the connector if needed"""
        raise NotImplementedError()

    def get_unread_messages_inbox(self) -> Iterable[Message]:
        """Get unread messages from the inbox"""
        raise NotImplementedError
