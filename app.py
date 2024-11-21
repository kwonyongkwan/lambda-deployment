import json
def lambda_handler(event,context):
    """
    HTTP 요청을 처리하는 AWS Lambda 함수
    """
    # 들어오는 이벤트 로그
    print("Event:", event)

    # 응답 메시지
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Hello from AWS Lambda!",
            "input": event
        })
    }

    return response