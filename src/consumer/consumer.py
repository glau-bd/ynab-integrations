from src.utils.constants import TOPIC_NAME, CONFIG_PATH
from src.consumer import logger
from argparse import ArgumentParser
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    config_parser = ConfigParser()
    config_parser.read_file(open(CONFIG_PATH))
    config = dict(config_parser["default"])
    config.update(config_parser["consumer"])

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    consumer.subscribe([TOPIC_NAME], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                logger.debug("Waiting...")
            elif msg.error():
                logger.error(msg.error())
            else:
                logger.info(
                    "Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                        topic=msg.topic(),
                        key=msg.key().decode("utf-8"),
                        value=msg.value().decode("utf-8"),
                    )
                )
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
