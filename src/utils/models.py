from re import sub
from datetime import datetime
from functools import cached_property
from typing import Optional, Union

from dataclasses import dataclass
from ynab_api.models import SaveTransaction


@dataclass
class Transaction:
    """
    Intermediary class that loads basic primitive types from a dict.
    """
    account_id: str
    timestamp: Union[int, float]
    amount: Optional[int] = None
    memo: Optional[str] = None
    payee_id: Optional[str] = None
    payee_name: Optional[str] = None
    category_id: Optional[str] = None
    cleared: Optional[bool] = None
    flag_color: Optional[str] = None
    approved: Optional[bool] = False

    def to_savetransaction(self) -> SaveTransaction:
        return SaveTransaction(
            account_id=self.account_id,
            date=datetime.fromtimestamp(self.timestamp),
            amount=self.amount,
            payee_id=self.payee_id,
            payee_name=self.payee_name,
            category_id=self.category_id,
            memo=self.memo,
            cleared=self.cleared,
            approved=self.approved,
        )

    def key(self) -> str:
        return f"{self.account_id}-{self.timestamp}-{self.amount}"


@dataclass(frozen=True)
class Message:
    body: str
    datetime: datetime

    @cached_property
    def replace_whitespace(self) -> str:
        body = self.body
        body = sub(r"\n", " ", body)
        body = sub(r"\s+", " ", body)
        return body
