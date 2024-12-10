import re
from decimal import Decimal
from logging import getLogger
from typing import Optional

from ..utils.models import Transaction, Message
from .base_parser import BaseMessageParser

logger = getLogger(__name__)


class UobGiroEmailParser(BaseMessageParser):
    pattern = re.compile(
        r"A transaction of SGD(\d*\.\d{2}) has been debited from your UOB account XXXXXX(\d{4}) on (\d{2}:\d{2}[APM]{2} \d{1,2}-\w{3}-\d{4}). Ref: Inward DR - GIRO, (.+)\. For assistance, call UOB customer service\."
    )
    accounts_section = "uob_giro_email_accounts"

    def accepts(self, message: Message) -> bool:
        return bool(self.pattern.search(message.replace_whitespace))

    def parse_message(self, message: Message) -> Optional[Transaction]:
        match = self.pattern.search(message.replace_whitespace)

        if not match:
            raise Exception("Message does not match pattern")
        amount: str = match.group(1)
        value = int(Decimal(amount) * -1000)
        account_num = match.group(2)
        payee = match.group(4)
        try:
            account_id = self.get_ynab_account_id(account_num)
            assert account_id, "Account ID is empty"
        except Exception as e:
            logger.warning(f"Failed to get YNAB account ID: {e}")
            return None

        return Transaction(
            account_id=account_id,
            amount=value,
            timestamp=message.datetime.timestamp(),
            payee_name=payee,
            memo=f"GIRO transaction to {payee}",
        )
