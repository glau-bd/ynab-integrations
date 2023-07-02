from configparser import ConfigParser
from typing import Any, Dict, Generator, Type

from src.connectors.base_connector import BaseConnector
from src.connectors.imap.imap_connector import ImapConnector
from src.utils.constants import CONNECTOR_CONFIG_PATH

CONNECTORS: Dict[str, Type[BaseConnector]] = {ImapConnector.__name__: ImapConnector}

config_parser = ConfigParser()
config_parser.read_file(open(CONNECTOR_CONFIG_PATH))


def get_connectors() -> Generator[BaseConnector, Any, None]:
    for section in config_parser.sections():
        connector_type = config_parser.get(section, "connector_type", fallback=None)
        if connector_type:
            connector_class = CONNECTORS[connector_type]
            connector = connector_class(**dict(config_parser[section]))
            yield connector


def get_active_connectors() -> Generator[BaseConnector, Any, None]:
    for connector in get_connectors():
        if connector.active is True:
            yield connector
