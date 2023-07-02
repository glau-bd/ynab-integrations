from typing import List

from src.message_parsers.base_parser import BaseMessageParser
from src.message_parsers.uob_paynow_email import UobPaynowEmailParser

message_parsers: List[BaseMessageParser] = [UobPaynowEmailParser()]
