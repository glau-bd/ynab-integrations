from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    Duration,
)
from constructs import Construct


class YnabIntegrationsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a lambda function
        lambda_fn: _lambda.Function = _lambda.Function(
            self,
            'ynabTransactionProcessor',
            code=_lambda.Code.from_asset('src'),
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="index.lambda_handler",
            timeout=Duration.seconds(30),
        )

        api = apigw.RestApi(
            self,
            "YNABIntegrationsApi",
            rest_api_name="TransactionAPI",
            description="This service serves as a webhook for banking notifications",
        )

        get_widgets_integration = apigw.LambdaIntegration(
            lambda_fn,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method("POST", get_widgets_integration)