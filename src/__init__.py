import os
import sys

IS_AWS = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None

if IS_AWS:
    from aws_lambda_powertools import Logger

    logger = Logger()
else:
    import logging

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
