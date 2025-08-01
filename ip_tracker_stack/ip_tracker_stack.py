from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
    aws_apigatewayv2_alpha as apigw,
    aws_apigatewayv2_integrations_alpha as integrations,
    aws_dynamodb as ddb,
)
from constructs import Construct
import os

class IpTrackerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        table = ddb.Table(
            self, "IpLogTable",
            partition_key={"name": "hash", "type": ddb.AttributeType.STRING},
            sort_key={"name": "timestamp", "type": ddb.AttributeType.STRING},
            removal_policy=ddb.RemovalPolicy.DESTROY
        )

        lambda_fn = lambda_.Function(
            self, "DynamicIpLoggerFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_handle_dynamic_ip_urls.handler",
            code=lambda_.Code.from_asset(os.path.dirname(__file__)),
            environment={
                "TABLE_NAME": table.table_name,
                "HASH_LIST": "AB12CD34,DEADBEEF,CAFEBABE,8BADF00D",
                "MANAGE_HASH": "ADMIN123"
            },
        )

        table.grant_read_write_data(lambda_fn)

        http_api = apigw.HttpApi(
            self, "IpTrackerApi",
            cors_preflight=apigw.CorsPreflightOptions(
                allow_methods=[apigw.CorsHttpMethod.ANY],
                allow_origins=["*"]
            )
        )

        integration = integrations.HttpLambdaIntegration("LambdaIntegration", lambda_fn)

        http_api.add_routes(
            path="/{proxy+}",
            methods=[apigw.HttpMethod.ANY],
            integration=integration
        )

        CfnOutput(self, "ApiUrl", value=http_api.api_endpoint)
