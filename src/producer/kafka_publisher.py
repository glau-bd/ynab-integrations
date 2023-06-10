import json
from configparser import ConfigParser

from confluent_kafka import Producer

from src.producer import logger
from src.utils.constants import CONFIG_PATH, TOPIC_NAME
from src.utils.models import Transaction

config_parser = ConfigParser()
config_parser.read_file(open(CONFIG_PATH))
config = dict(config_parser["default"])

PRODUCER = Producer(config)


def delivery_callback(err, msg):
    if err:
        logger.error("Message failed delivery: {}".format(err))
    else:
        logger.info(
            "Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(),
                key=msg.key().decode("utf-8"),
                value=msg.value().decode("utf-8"),
            )
        )


def publish_message(transaction: Transaction):
    PRODUCER.produce(
        topic=TOPIC_NAME,
        key=transaction.key(),
        value=json.dumps(transaction.json()).encode("utf-8"),
        callback=delivery_callback,
    )
    PRODUCER.poll(300)
    PRODUCER.flush()
