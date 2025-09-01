import os

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb, RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,

)
from constructs import Construct

LAMBDA_BUILD_PATH = os.path.join(os.path.dirname(__file__), "..", "build", "lambda")

class SharedResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.shoes_table = dynamodb.Table(
            self, "ShoesTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.shoes_table.add_global_secondary_index(
            index_name="brand-index",
            partition_key=dynamodb.Attribute(name="brand", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL
        )

        self.orders_table = dynamodb.Table(
            self, "OrdersTable",
            partition_key=dynamodb.Attribute(name="orderId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.orders_table.add_global_secondary_index(
            index_name="username-index",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING)
        )

        self.invoices_bucket = s3.Bucket(
            self, "InvoicesBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

class ListShoesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, shared_resources: SharedResourceStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.list_shoes_lambda = _lambda.Function(
            self, "ListShoesFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="list_shoes.handler",
            code=_lambda.Code.from_asset(LAMBDA_BUILD_PATH),
            environment={
                "SHOES_TABLE_NAME": shared_resources.shoes_table.table_name
            }
        )

        shared_resources.shoes_table.grant_read_data(self.list_shoes_lambda)


class OrdersAPIStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, shared_resources: SharedResourceStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.create_order_lambda = _lambda.Function(
            self, "CreateOrderFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="create_order.handler",
            code=_lambda.Code.from_asset(LAMBDA_BUILD_PATH),
            environment={
                "SHOES_TABLE_NAME": shared_resources.shoes_table.table_name,
                "ORDERS_TABLE_NAME": shared_resources.orders_table.table_name,
                "INVOICES_BUCKET_NAME": shared_resources.invoices_bucket.bucket_name
            }
        )

        self.list_orders_by_username_lambda = _lambda.Function(
            self, "ListOrdersByUsernameFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="list_order_by_username.handler",
            code=_lambda.Code.from_asset(LAMBDA_BUILD_PATH),
            environment={
                "ORDERS_TABLE_NAME": shared_resources.orders_table.table_name,
            }
        )

        shared_resources.shoes_table.grant_read_data(self.create_order_lambda)
        shared_resources.orders_table.grant_write_data(self.create_order_lambda)
        shared_resources.invoices_bucket.grant_put(self.create_order_lambda)
        shared_resources.orders_table.grant_read_data(self.list_orders_by_username_lambda)


class APIGatewayStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,
                 list_shoes_stack: ListShoesStack,
                 orders_api_stack: OrdersAPIStack,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(self, "ShoeStoreApi", rest_api_name="ShoesStoreAPI")

        # /shoes endpoint
        shoes_resource = api.root.add_resource("shoes")
        shoes_resource.add_method("GET", apigateway.LambdaIntegration(list_shoes_stack.list_shoes_lambda),
                                  authorization_type=apigateway.AuthorizationType.NONE)

        # /orders endpoint
        orders_resource = api.root.add_resource("orders")
        orders_resource.add_method("POST", apigateway.LambdaIntegration(orders_api_stack.create_order_lambda),
                                   authorization_type=apigateway.AuthorizationType.NONE)

        # /orders/{username} endpoint
        orders_by_user_resource = orders_resource.add_resource("{username}")
        orders_by_user_resource.add_method("GET", apigateway.LambdaIntegration(orders_api_stack.list_orders_by_username_lambda),
                                           authorization_type=apigateway.AuthorizationType.NONE)
