import re
from datetime import datetime
from decimal import Decimal
from logging import getLogger
from typing import Optional

from ..utils.models import Transaction
from .base_parser import BaseMessageParser

logger = getLogger(__name__)


class UobAtmEmailParser(BaseMessageParser):
    pattern = re.compile(
        r"ATM Cash Withdrawal of SGD(\d*\.\d{2}) was performed on your UOB account ending with ([\d]+) at (\d{2}:\d{2}[APM]{2} \d{2}\/\d{2}\/\d{4})\."
    )
    accounts_section = "uob_atm_email_accounts"

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
        account_num = match.group(2)
        transaction_date = match.group(3)
        try:
            transaction_datetime = datetime.strptime(
                transaction_date, "%I:%M%p %d/%m/%Y"
            )
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
            account_id = self.get_ynab_account_id(account_num)
            assert account_id, "Account ID is empty"
        except Exception as e:
            logger.warning("Failed to get YNAB account ID")
            return None

        return Transaction(
            account_id=account_id,
            amount=value,
            timestamp=transaction_datetime.timestamp(),
            memo="ATM Withdrawal",
        )
