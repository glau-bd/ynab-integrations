import re
from datetime import datetime
from decimal import Decimal
from logging import getLogger
from typing import Optional

from dateutil import parser

from ..utils.models import Transaction
from .base_parser import BaseMessageParser

logger = getLogger(__name__)


class UobCardEmailParser(BaseMessageParser):
    pattern = re.compile(
        r"A transaction of SGD (\d*\.\d{2}) was made with your UOB Card ending ([\d]+) on (\d{2}/\d{2}/\d{2}) at ([A-Za-z/\s\d]+)\."
    )
    accounts_section = "uob_card_email_accounts"

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
        card_num = match.group(2)
        transaction_date = match.group(3)
        payee = match.group(4)
        try:
            transaction_datetime = datetime.strptime(transaction_date, "%d/%m/%y")
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
            account_id = self.get_ynab_account_id(card_num)
            assert account_id, "Account ID is empty"
        except Exception as e:
            logger.warning("Failed to get YNAB account ID")
            return None

        return Transaction(
            account_id=account_id,
            amount=value,
            timestamp=transaction_datetime.timestamp(),
            payee_name=payee,
        )
