from src.producer.kafka_publisher import publish_message
from src.utils.models import Transaction

a = Transaction(account_id="1", amount=1, timestamp=1)
publish_message(a)
