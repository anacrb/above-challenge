#!/usr/bin/env python3
import os

import aws_cdk as cdk

from above_challenge.above_challenge_stack import (
    SharedResourceStack,
    ListShoesStack,
    CreateOrderStack,
    ListOrdersByUsernameStack
)


app = cdk.App()

#  --- Shared stack ---
# This stack creates the shared infratructure, such as dynamodb, s3 and API Gateway
shared_stack = SharedResourceStack(app, "SharedResourceStack")

# --- Lambda stacks ---
# Independent stacks that create a lambda function. Depends on shared stack.
ListShoesStack(app, "ListShoesStack", shared_stack)
CreateOrderStack(app, "CreateOrderStack", shared_stack)
ListOrdersByUsernameStack(app, "ListOrdersByUsernameStack", shared_stack)

app.synth()
