from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    CfnOutput,
    aws_iam as iam
)
from constructs import Construct

class FlaskApiInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a dynamoDB table
        table = dynamodb.Table(self, "to_do_table",
            partition_key=dynamodb.Attribute(name="task_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )


        # Create secondary global index inside "to_do_table" to access users data
        table.add_global_secondary_index(
            # column name
            index_name="user_index",
            partition_key=dynamodb.Attribute(
            name="user_id",
            type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
            name="created_time",
            type=dynamodb.AttributeType.NUMBER
            )
        )

        # Create IAM role to allow lambda to access  
        lambda_role = iam.Role(self, "Lambda_role_dynamodb",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Attach permission to the IAM role
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:*"],
                resources=[table.table_arn]
            )
        )

        # Create Labmda function to execute API calls
        api_lambda = lambda_.Function(self, "api_lambda_function",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code = lambda_.Code.from_asset("../API/lambda_function.zip"),                  
            handler= "api.handler",
            environment={
                "TABLE_NAME": table.table_name
            },
            role=lambda_role
        )

        # Allow lambda function to access dynamoDB table
        table.grant_read_write_data(api_lambda)

        # Create URL endpoint for lambda function
        api_lambda_url = api_lambda.add_function_url(
            auth_type = lambda_.FunctionUrlAuthType.NONE,
            cors = lambda_.FunctionUrlCorsOptions
            (
                allowed_origins= ["*"],
                allowed_methods=[lambda_.HttpMethod.ALL],
                allowed_headers=["*"]
            )
        )

        # Output lambda function URL
        CfnOutput(self, "api_lambda_url_output",
            value=api_lambda_url.url
        )
        

        