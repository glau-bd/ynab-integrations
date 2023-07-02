import logging
import sys
from configparser import ConfigParser
from typing import Generator, List, Optional

from ynab_api import ApiClient, ApiException, Configuration
from ynab_api.api.transactions_api import TransactionsApi
from ynab_api.models import SaveTransaction, SaveTransactionsWrapper

from src.connectors import get_active_connectors
from src.message_parsers import BaseMessageParser, message_parsers
from src.utils.constants import YNAB_CONFIG_PATH
from utils.models import Transaction

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

config_parser = ConfigParser()
config_parser.read_file(open(YNAB_CONFIG_PATH))

YNAB_ACCESS_TOKEN = config_parser["auth"]["YNAB_ACCESS_TOKEN"]
YNAB_BUDGET_ID = config_parser["auth"]["YNAB_BUDGET_ID"]
YNAB_API_BASE_URL = config_parser["auth"]["YNAB_API_BASE_URL"]
SUCCESS = {"statusCode": 200}

CONFIGURATION = Configuration(
    host=YNAB_API_BASE_URL,
    api_key={"bearer": YNAB_ACCESS_TOKEN},
    api_key_prefix={"bearer": "Bearer"},
)


def fetch_messages() -> Generator[str, None, None]:
    """Fetch messages from all active connectors."""
    for connector in get_active_connectors():
        for message in connector.get_unread_messages_inbox():
            yield message


def parse_message(message: str) -> Optional[Transaction]:
    """Parse a message using the first parser that accepts it."""
    parser: Optional[BaseMessageParser] = None
    parser = next(
        (parser for parser in message_parsers if parser.accepts(message)), None
    )
    if parser is None:
        logger.warning(
            f"No message parser found for message {message[:100]}..., skipping"
        )
        return None
    transaction = parser.parse_message(message)
    logger.info(f"Transaction: {transaction}")
    return transaction


def write_transactions(transactions: List[SaveTransaction]):
    """
    Send a list of SaveTransaction objects to YNAB

    Args:
        transactions (List[SaveTransaction]): List of SaveTransaction objects

    Raises:
        e: ApiException
    """
    with ApiClient(CONFIGURATION) as api_client:
        api_instance = TransactionsApi(api_client)
        data = SaveTransactionsWrapper(transactions=transactions)

        try:
            api_response = api_instance.create_transaction(YNAB_BUDGET_ID, data)
            logger.info(api_response)
        except ApiException as e:
            logger.exception(e)


def lambda_handler(event, context):
    """Fetch all messages, parse them, and write them to YNAB."""
    transactions: List[Transaction] = []
    for message in fetch_messages():
        transaction = parse_message(message)
        if transaction is not None:
            transactions.append(transaction)
    write_transactions([t.to_savetransaction() for t in transactions])

    return SUCCESS
