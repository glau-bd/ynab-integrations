import re
from logging import getLogger
from typing import Optional

from ..utils.models import Transaction, Message
from .base_parser import BaseMessageParser

logger = getLogger(__name__)


class UobFastEmailParser(BaseMessageParser):
    pattern = re.compile(
        r"UOB-Your FAST funds transfer to (.+) on (\d{2}-[A-Za-z]{3}-\d{4}) is successful"
    )
    accounts_section = "uob_fast_email_accounts"

    def accepts(self, message: Message) -> bool:
        return bool(self.pattern.search(message.replace_whitespace))

    def parse_message(self, message: Message) -> Optional[Transaction]:
        match = self.pattern.search(message.replace_whitespace)

        if not match:
            raise Exception("Message does not match pattern")
        payee = match.group(1)
        try:
            account_id = self.get_ynab_account_id()
            assert account_id, "Account ID is empty"
        except Exception as e:
            logger.warning(f"Failed to get YNAB account ID: {e}")
            return None

        return Transaction(
            account_id=account_id,
            amount=None,
            timestamp=message.datetime.timestamp(),
            payee_name=payee,
        )
