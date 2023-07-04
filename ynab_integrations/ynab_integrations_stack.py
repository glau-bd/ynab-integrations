import os

from aws_cdk import Duration, Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as _lambda_alpha
from constructs import Construct


class YnabIntegrationsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        _lambda_alpha.PythonFunction(
            self,
            "ynabTransactionProcessor",
            entry=".",
            index="src/index.py",
            handler="lambda_handler",
            timeout=Duration.seconds(60),
            bundling=_lambda_alpha.BundlingOptions(
                asset_excludes=[
                    path
                    for path in os.listdir(".")
                    if path not in ["src", "poetry.lock", "pyproject.toml"]
                ]
            ),
            runtime=_lambda.Runtime.PYTHON_3_10,
        )
