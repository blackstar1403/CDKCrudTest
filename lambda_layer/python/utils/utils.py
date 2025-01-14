import json, re, boto3


# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")

# Allowed Status
ALLOWED_STATUS = ["pending", "in-progress", "completed"]

# Regex for validating strings
STR_REGEX = re.compile(r"^[\w\s-]{1,255}$")


def validate_request_body(body: dict, required_keys: list):
    """
    Validate if the request for tasks is correct.
    """
    missing_keys = [key for key in required_keys if key not in body]
    # Validation if some key is missing
    if missing_keys:
        return {
            "statusCode" : 400,
            "body" : json.dumps({"error": f"Missing required keys: {', '.join(missing_keys)}"})
        }
    
    # Validation if some value is wrong writted
    for key in required_keys:
        value = body[key]
        if not isinstance(value, str) or not STR_REGEX.match(value):
            return {
                "statusCode": 400,
                "body": json.dumps({"error" : f"'{key}' must be a valid string"})
            } 
    
    # Validation for allowed status
    if "status" in body and body["status"] not in ALLOWED_STATUS:
        return {
            "statusCode": 400,
            "body": json.dumps({"error" : f"The status must be one of these: {', '.join(ALLOWED_STATUS)}"})
        }
    
    return None


def task_exists(task_id: str, table_name: str):
    """
    Verify if a task with the given task_id exists
    """
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"taskId": task_id})
    response = response.get("Item", None)

    return response