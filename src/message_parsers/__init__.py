from typing import List

from .base_parser import BaseMessageParser
from .uob_card_email import UobCardEmailParser
from .uob_paynow_email import UobPaynowEmailParser

message_parsers: List[BaseMessageParser] = [
    UobPaynowEmailParser(),
    UobCardEmailParser(),
]
