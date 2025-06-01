import boto3
import os
import json

SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT", "your-sagemaker-endpoint-name")

async def invoke_sagemaker_model(payload: dict) -> dict:
    """
    Invoke a deployed SageMaker endpoint asynchronously (sync boto3 call wrapped for demo).
    """
    client = boto3.client("sagemaker-runtime")
    response = client.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT,
        ContentType="application/json",
        Body=json.dumps(payload)
    )
    result = response["Body"].read().decode()
    return json.loads(result)
