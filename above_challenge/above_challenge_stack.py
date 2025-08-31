import os

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb, RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,

)
from constructs import Construct

class AboveChallengeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        shoes_table = dynamodb.Table(
            self, "ShoesTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        shoes_table.add_global_secondary_index(
            index_name="brand-index",
            partition_key=dynamodb.Attribute(name="brand", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL
        )

        orders_table = dynamodb.Table(
            self, "OrdersTable",
            partition_key=dynamodb.Attribute(name="orderId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        orders_table.add_global_secondary_index(
            index_name="username-index",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING)
        )

        invoices_bucket = s3.Bucket(
            self, "InvoicesBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True # For easy cleanup
        )

        lambda_code_path = os.path.join(os.path.dirname(__file__), "..", "build", "lambda")

        list_shoes_lambda = _lambda.Function(
            self, "ListShoesFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="list_shoes.handler",
            code=_lambda.Code.from_asset(lambda_code_path),
            environment={
                "SHOES_TABLE_NAME": shoes_table.table_name
            }
        )

        create_order_lambda = _lambda.Function(
            self, "CreateOrderFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="create_order.handler",
            code=_lambda.Code.from_asset(lambda_code_path),
            environment={
                "SHOES_TABLE_NAME": shoes_table.table_name,
                "ORDERS_TABLE_NAME": orders_table.table_name,
                "INVOICES_BUCKET_NAME": invoices_bucket.bucket_name
            }
        )

        list_orders_by_username_lambda = _lambda.Function(
            self, "ListOrdersByUsernameFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="list_orders_by_username.handler",
            code=_lambda.Code.from_asset(lambda_code_path),
            environment={
                "ORDERS_TABLE_NAME": orders_table.table_name,
            }
        )

        # Permissions
        shoes_table.grant_read_data(list_shoes_lambda)
        shoes_table.grant_read_data(create_order_lambda)
        orders_table.grant_write_data(create_order_lambda)
        invoices_bucket.grant_put(create_order_lambda)
        orders_table.grant_read_data(list_orders_by_username_lambda)

        #API Gateway
        api = apigateway.RestApi(self, "ShoeStoreApi")

        # /shoes endpoint
        shoes_resource = api.root.add_resource("shoes")
        shoes_resource.add_method("GET", apigateway.LambdaIntegration(list_shoes_lambda),
                                  authorization_type=apigateway.AuthorizationType.NONE)

        # /orders endpoint
        orders_resource = api.root.add_resource("orders")
        orders_resource.add_method("POST", apigateway.LambdaIntegration(create_order_lambda),
                                   authorization_type=apigateway.AuthorizationType.NONE)

        # /orders/{username} endpoint
        orders_by_user_resource = orders_resource.add_resource("{username}")
        orders_by_user_resource.add_method("GET", apigateway.LambdaIntegration(list_orders_by_username_lambda),
                                           authorization_type=apigateway.AuthorizationType.NONE)
