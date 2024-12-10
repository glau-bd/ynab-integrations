import re
from decimal import Decimal
from logging import getLogger
from typing import Optional

from ..utils.models import Transaction, Message
from .base_parser import BaseMessageParser

logger = getLogger(__name__)


class UobPaynowEmailParser(BaseMessageParser):
    pattern = re.compile(
        r"You made a PayNow transfer of SGD (\d*\.\d{2}) to PayNow ID ending with ([\w]+) at ([\d:]+[APM]+), ([\d]+-[A-Za-z]+-\d+)"
    )
    accounts_section = "uob_paynow_email_accounts"

    def accepts(self, message: Message) -> bool:
        return bool(self.pattern.search(message.replace_whitespace))

    def parse_message(self, message: Message) -> Optional[Transaction]:
        match = self.pattern.search(message.replace_whitespace)

        if not match:
            raise Exception("Message does not match pattern")
        amount: str = match.group(1)
        value = int(Decimal(amount) * -1000)
        paynow_id = match.group(2)
        try:
            account_id = self.get_ynab_account_id()
            assert account_id, "Account ID is empty"
        except Exception as e:
            logger.warning(f"Failed to get YNAB account ID: {e}")
            return None

        return Transaction(
            account_id=account_id,
            amount=value,
            timestamp=message.datetime.timestamp(),
            memo=f"Paynow transaction to {paynow_id}",
            payee_name=paynow_id,
        )
