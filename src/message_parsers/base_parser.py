import logging
import re
from abc import ABC, abstractmethod
from configparser import ConfigParser
from typing import Optional

import pytz

from ..utils.constants import YNAB_CONFIG_PATH
from ..utils.models import Transaction

logger = logging.getLogger(__name__)
config_parser = ConfigParser()
config_parser.read_file(open(YNAB_CONFIG_PATH))


class BaseMessageParser(ABC):
    """Base class that parses message contents using regex parsing"""

    pattern: re.Pattern
    accounts_section: str

    @abstractmethod
    def accepts(self, message: str) -> bool:
        """Check if the message is accepted by the parser"""
        raise NotImplementedError()

    @classmethod
    def replace_whitespace(cls, message: str) -> str:
        message = re.sub(r"\n", " ", message)
        message = re.sub(r"\s+", " ", message)
        return message

    @abstractmethod
    def parse_message(self, message: str) -> Optional[Transaction]:
        raise NotImplementedError()

    def get_ynab_account_id(self, banking_account_identier: str = "default") -> str:
        return config_parser[self.accounts_section][banking_account_identier]

    def get_timezone(self, default_tz: str):
        try:
            return pytz.timezone(config_parser[self.accounts_section]["timezone"])
        except Exception:
            return pytz.timezone(default_tz)
