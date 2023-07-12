import re
from datetime import datetime
from decimal import Decimal
from logging import getLogger
from typing import Optional

from dateutil import parser

from ..utils.models import Transaction
from .base_parser import BaseMessageParser

logger = getLogger(__name__)


class UobPaynowEmailParser(BaseMessageParser):
    pattern = re.compile(
        r"You made a PayNow transfer of .* (\d*\.\d{2}) to PayNow ID ending with ([\w]+) at ([\d:]+[APM]+), ([\d]+-[A-Za-z]+-\d+)"
    )
    accounts_section = "uob_paynow_email_accounts"

    def accepts(self, message: str) -> bool:
        message = self.replace_whitespace(message)
        return bool(self.pattern.search(message))

    def parse_message(self, message: str) -> Optional[Transaction]:
        message = self.replace_whitespace(message)
        match = self.pattern.search(message)

        if not match:
            raise Exception("Message does not match pattern")
        amount: str = match.group(1)
        value = int(Decimal(amount) * -1000)
        paynow_id = match.group(2)
        transaction_datetime = match.group(3) + ", " + match.group(4)
        try:
            transaction_datetime = parser.parse(transaction_datetime, fuzzy=True)
            transaction_datetime = self.get_timezone("Asia/Singapore").localize(
                transaction_datetime
            )
        except Exception as e:
            logger.warning(
                "Failed to parse transaction datetime, using current time instead"
            )
            logger.exception(e)
            transaction_datetime = datetime.now()
        try:
            account_id = self.get_ynab_account_id("default")
            assert account_id, "Account ID is empty"
        except Exception as e:
            logger.warning("Failed to get YNAB account ID")
            return None

        return Transaction(
            account_id=account_id,
            amount=value,
            timestamp=transaction_datetime.timestamp(),
            memo=f"Paynow transaction to {paynow_id}",
            payee_name=paynow_id,
        )
