from typing import Generator

from imap_tools import MailBox

from ..base_connector import BaseConnector


class ImapConnector(BaseConnector):
    host: str
    user: str
    password: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.host = kwargs["host"]
            self.user = kwargs["user"]
            self.password = kwargs["password"]
        except KeyError as e:
            raise ValueError("Missing required argument") from e

    def get_unread_messages_inbox(self) -> Generator[str, None, None]:
        """Get unread messages from the inbox, and mark as read"""
        with MailBox(self.host).login(self.user, self.password) as mailbox:
            for msg in mailbox.fetch(
                criteria="UNSEEN",
            ):
                yield msg.text
