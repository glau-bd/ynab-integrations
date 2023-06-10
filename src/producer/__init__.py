import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s",
)

logger = logging.getLogger("producer")
