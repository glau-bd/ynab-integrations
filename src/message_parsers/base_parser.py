import logging
import re
from abc import ABC, abstractmethod
from configparser import ConfigParser

from src.utils.constants import YNAB_CONFIG_PATH
from src.utils.models import Transaction

logger = logging.getLogger(__name__)
config_parser = ConfigParser()
config_parser.read_file(open(YNAB_CONFIG_PATH))


class BaseMessageParser(ABC):
    """Base class that parses message contents using regex parsing"""

    pattern: re.Pattern

    @abstractmethod
    def accepts(self, message: str) -> bool:
        """Check if the message is accepted by the parser"""
        raise NotImplementedError()

    @abstractmethod
    def parse_message(self, message: str) -> Transaction:
        raise NotImplementedError()

    def get_ynab_account_id(self, banking_account_identier: str) -> str:
        return config_parser["accounts"][banking_account_identier]
