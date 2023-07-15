from typing import List

from .base_parser import BaseMessageParser
from .uob_atm_email import UobAtmEmailParser
from .uob_giro_email import UobGiroEmailParser
from .uob_paynow_email import UobPaynowEmailParser
from .uob_fast_email import UobFastEmailParser
from .uob_card_email import UobCardEmailParser

message_parsers: List[BaseMessageParser] = [
    UobAtmEmailParser(),
    UobGiroEmailParser(),
    UobPaynowEmailParser(),
    UobFastEmailParser(),
    UobCardEmailParser(),
]
