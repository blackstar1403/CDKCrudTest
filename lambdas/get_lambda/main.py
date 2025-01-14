import json, os, boto3
from utils.utils import task_exists


# Initialize DynamoDB client with boto3
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])

def lambda_handler(event, __):
    try:
        # Get the path parameters
        parameters = event.get("pathParameters")

        # Validate if task_id is in the url
        if parameters and "task_id" in parameters:
            task_id = parameters["task_id"]

            # Validate if task exists
            if not task_exists(task_id, os.environ["DYNAMO_TABLE"]):
                return{
                    "statusCode": 404,
                    "body": json.dumps({"error" : "Task not found"})           
                }
            
            response = table.get_item(Key={"taskId": task_id})
            return {
                "statusCode": 200,
                "body": json.dumps(response["Item"])
            }
        
        else: # Task id doesnt provided
            response = table.scan()
            tasks = response.get("Items", [])
            
            return {
                "statusCode": 200,
                "body": json.dumps(tasks)
            }
        
    except Exception as e:
        return{
            "statusCode": 500,
            "body": json.dumps({"error" : str(e)})           
        }