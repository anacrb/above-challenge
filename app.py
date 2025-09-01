#!/usr/bin/env python3
import os

import aws_cdk as cdk

from above_challenge.above_challenge_stack import (
    SharedResourceStack,
    ListShoesStack,
    OrdersAPIStack,
    APIGatewayStack
)


app = cdk.App()

#  --- Shared stack ---
# This stack creates the shared infratructure, such as dynamodb, s3 and API Gateway
shared_stack = SharedResourceStack(app, "SharedResourceStack")

# --- Lambda stacks ---
# Independent stacks that create a lambda function. Depends on shared stack.
list_shoes_stack = ListShoesStack(app, "ListShoesStack", shared_stack)
orders_api_stack = OrdersAPIStack(app, "OrdersAPIStack", shared_stack)

# --- API Gateway stack ---
# Initialize the API Gateway

api_stack = APIGatewayStack(app, "APIGatewayStack", list_shoes_stack, orders_api_stack)

app.synth()
