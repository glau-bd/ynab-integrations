from configparser import ConfigParser
from typing import Any, Dict, Generator, Type

from ..utils.constants import CONNECTOR_CONFIG_PATH
from .base_connector import BaseConnector
from .imap.imap_connector import ImapConnector

CONNECTORS: Dict[str, Type[BaseConnector]] = {ImapConnector.__name__: ImapConnector}

config_parser = ConfigParser()
config_parser.read_file(open(CONNECTOR_CONFIG_PATH))


def get_connectors() -> Generator[BaseConnector, Any, None]:
    for section in config_parser.sections():
        connector_type = config_parser.get(section, "connector_type", fallback=None)
        if connector_type:
            connector_class = CONNECTORS[connector_type]
            active = config_parser.get(section, "active", fallback="false")
            connector = connector_class(
                name=section, active=active, **dict(config_parser[section])
            )
            yield connector


def get_active_connectors() -> Generator[BaseConnector, Any, None]:
    for connector in get_connectors():
        if connector.active is True:
            yield connector
