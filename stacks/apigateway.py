import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_apigateway as apigateway
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion


class ApiGatewayStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, dynamodb_table, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define lambda layer for validations
        validations_layer = LayerVersion(
            self, "ValidationLayerPython312",
            layer_version_name="ValidationLayerPython312",
            code=Code.from_asset("lambda_layer"),
            compatible_runtimes=[Runtime.PYTHON_3_12],
            description="Layer with validations for tasks CRUD"
        )

        # Define lambda for GET
        get_task_lambda =Function(
            self, "GetTaskFunction",
            function_name="GetTaskFunction",
            runtime=Runtime.PYTHON_3_12,
            handler="main.lambda_handler",
            code=Code.from_asset("lambdas/get_lambda"),
            environment={"DYNAMO_TABLE": dynamodb_table.table_name},
            layers=[validations_layer]
        )

        # Define lambda for UPDATE
        update_task_lambda =Function(
            self, "UpdateTaskFunction",
            function_name="UpdateTaskFunction",
            runtime=Runtime.PYTHON_3_12,
            handler="main.lambda_handler",
            code=Code.from_asset("lambdas/update_lambda"),
            environment={"DYNAMO_TABLE": dynamodb_table.table_name},
            layers=[validations_layer]
        )

        # Define lambda for CREATE
        create_task_lambda =Function(
            self, "CreateTaskFunction",
            function_name="CreateTaskFunction",
            runtime=Runtime.PYTHON_3_12,
            handler="main.lambda_handler",
            code=Code.from_asset("lambdas/create_lambda"),
            environment={"DYNAMO_TABLE": dynamodb_table.table_name},
            layers=[validations_layer]
        )

        # Define lambda for DELETE
        delete_task_lambda =Function(
            self, "DeleteTaskFunction",
            function_name="DeleteTaskFunction",
            runtime=Runtime.PYTHON_3_12,
            handler="main.lambda_handler",
            code=Code.from_asset("lambdas/delete_lambda"),
            environment={"DYNAMO_TABLE": dynamodb_table.table_name},
            layers=[validations_layer]
        )

        # Grant Read only permissions to GET Lambda
        dynamodb_table.grant_read_data(get_task_lambda)

        # Grant Read and write permissions to CREATE Lambda
        dynamodb_table.grant_read_write_data(create_task_lambda)

        # Grant Read and write permissions to UPDATE Lambda
        dynamodb_table.grant_read_write_data(update_task_lambda)

        # Grant Read and write permissions to DELETE Lambda
        dynamodb_table.grant_read_write_data(delete_task_lambda)

        # Define Api Gateway
        api = apigateway.RestApi(self, "TasksApi")

        # Define endpoints
        tasks_resource = api.root.add_resource("tasks")
        tasks_resource.add_method("GET", apigateway.LambdaIntegration(get_task_lambda)) # List all tasks
        tasks_resource.add_method("POST", apigateway.LambdaIntegration(create_task_lambda)) # Create a new tasks

        task_resource = tasks_resource.add_resource("{task_id}")
        task_resource.add_method("GET", apigateway.LambdaIntegration(get_task_lambda)) # Get a especific task
        task_resource.add_method("PUT", apigateway.LambdaIntegration(update_task_lambda)) # Update a especific task
        task_resource.add_method("DELETE", apigateway.LambdaIntegration(delete_task_lambda)) # Delete a especific task