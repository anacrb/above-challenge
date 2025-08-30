import aws_cdk as core
import aws_cdk.assertions as assertions

from above_challenge.above_challenge_stack import AboveChallengeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in above_challenge/above_challenge_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AboveChallengeStack(app, "above-challenge")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
