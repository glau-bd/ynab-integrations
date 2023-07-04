import os

from aws_cdk import Duration, Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as lambda_alpha_
from constructs import Construct


class YnabIntegrationsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_function: lambda_alpha_.PythonFunction = lambda_alpha_.PythonFunction(
            self,
            "ynabTransactionProcessor",
            entry=".",
            index="src/index.py",
            handler="lambda_handler",
            timeout=Duration.seconds(60),
            bundling=lambda_alpha_.BundlingOptions(
                asset_excludes=[
                    path
                    for path in os.listdir(".")
                    if path not in ["src", "poetry.lock", "pyproject.toml"]
                ]
            ),
            runtime=lambda_.Runtime.PYTHON_3_10,
        )
        # create an hourly rule
        event_rule = events.Rule(
            self,
            "ynabTransactionProcessorRule",
            schedule=events.Schedule.rate(Duration.hours(1)),
        )
        event_rule.add_target(targets.LambdaFunction(lambda_function))
