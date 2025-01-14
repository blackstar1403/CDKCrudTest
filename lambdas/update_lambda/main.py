import json, os, boto3
from utils.utils import validate_request_body, task_exists


# Initialize DynamoDB client with boto3
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])

def lambda_handler(event, __):
    try:
        # Parse the request body
        body = json.loads(event["body"])
        
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
            
        else: # Task id doesnt provided
            return {
                "statusCode": 400,
                "body": json.dumps({"error" : "Task ID is required"})
            }
        
        # Validate if request is correct
        error = validate_request_body(body, ["title", "description", "status"])
        if error:
            return error
        
        # Update task item
        response = table.update_item(
            Key={"taskId": task_id},
            UpdateExpression="SET #title = :title, #description = :desc, #status = :status",
            # Use aliases because status is a reserved word in DynamoDB
            ExpressionAttributeNames={
                "#title": "title",
                "#description": "description",
                "#status": "status",
            },
            ExpressionAttributeValues={
                ":title": body["title"],
                ":desc": body["description"],
                ":status": body["status"],
            },
            ReturnValues="ALL_NEW"
        )
        return {
            "statusCode": 200,
            "body": json.dumps(response["Attributes"])
        }
    
    except Exception as e:
        return{
            "statusCode": 500,
            "body": json.dumps({"error" : str(e)})           
        }