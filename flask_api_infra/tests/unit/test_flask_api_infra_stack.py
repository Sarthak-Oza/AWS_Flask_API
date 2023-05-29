import aws_cdk as core
import aws_cdk.assertions as assertions

from flask_api_infra.flask_api_infra_stack import FlaskApiInfraStack

# example tests. To run these tests, uncomment this file along with the example
# resource in flask_api_infra/flask_api_infra_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FlaskApiInfraStack(app, "flask-api-infra")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
