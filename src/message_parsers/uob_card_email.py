import re
from decimal import Decimal
from logging import getLogger
from typing import Optional

from ..utils.models import Transaction, Message
from .base_parser import BaseMessageParser

logger = getLogger(__name__)


class UobCardEmailParser(BaseMessageParser):
    pattern = re.compile(
        r"A transaction of SGD (\d*\.\d{2}) was made with your UOB Card ending ([\d]+) on (\d{2}\/\d{2}\/\d{2}) at (.+)\. If unauthorised, call 24\/7 Fraud Hotline now"
    )
    accounts_section = "uob_card_email_accounts"

    def accepts(self, message: Message) -> bool:
        return bool(self.pattern.search(message.replace_whitespace))

    def parse_message(self, message: Message) -> Optional[Transaction]:
        match = self.pattern.search(message.replace_whitespace)

        if not match:
            raise Exception("Message does not match pattern")
        amount: str = match.group(1)
        value = int(Decimal(amount) * -1000)
        card_num = match.group(2)
        payee = match.group(4)
        try:
            account_id = self.get_ynab_account_id(card_num)
            assert account_id, "Account ID is empty"
        except Exception as e:
            logger.warning(f"Failed to get YNAB account ID: {e}")
            return None

        return Transaction(
            account_id=account_id,
            amount=value,
            timestamp=message.datetime.timestamp(),
            payee_name=payee,
        )
