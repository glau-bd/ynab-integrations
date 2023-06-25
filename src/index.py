def lambda_handler(event, context):
    print(f"Received message: {event}")
    
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
    }
    return response
