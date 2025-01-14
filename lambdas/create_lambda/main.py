import json, os, uuid, boto3
from utils.utils import validate_request_body


# Initialize DynamoDB client with boto3
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])

def lambda_handler(event, __):
    try:
        # Parse the request body
        body = json.loads(event["body"])

        # Validate if request is correct
        error = validate_request_body(body, ["title", "description", "status"])
        if error:
            return error
        # Generate unique ID
        task_id = str(uuid.uuid4())

        # Create task item
        item = {
            "taskId" : task_id,
            "title": body["title"],
            "description": body["description"],
            "status": body["status"]
        }

        # Insert it into dynamodb
        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps(item)
        }
    except Exception as e:
        return{
            "statusCode": 500,
            "body": json.dumps({"error" : str(e)})           
        }