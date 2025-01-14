import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_dynamodb import TableV2, Attribute, AttributeType, Billing


class DynamoDbStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define our Tasks DynamoDB table
        self.tasks_table = TableV2(
            self, "TasksTable",
            table_name="TasksTable",
            partition_key=Attribute(name="taskId", type=AttributeType.STRING),
            billing=Billing.on_demand(),
            removal_policy=cdk.RemovalPolicy.DESTROY
        ) 