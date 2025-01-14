import aws_cdk as cdk
from stacks.dynamodb import DynamoDbStack
from stacks.apigateway import ApiGatewayStack

app = cdk.App()

# Task Table DynamoDB Stack
dynamodb_stack = DynamoDbStack(app, "DynamoDBStackTasks")

# CRUD Api Gateway Stack 
api_gateway_stack = ApiGatewayStack(
    app, "ApiGatewayStackTasks",
    dynamodb_table=dynamodb_stack.tasks_table
)

app.synth()