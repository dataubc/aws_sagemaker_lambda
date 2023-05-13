import os
import io
import boto3
import json
import csv
runtime_client= boto3.client('runtime.sagemaker')
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']



def convert_payload_to_csv(payload):
    csv_data = ""
    for row in payload:
        str_row = ",".join(map(str, row)) + "\n"
        csv_data += str_row
    return csv_data.strip()
    
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)
    
    # Convert the payload to CSV format
    payload_csv = convert_payload_to_csv(payload)
    
    response = runtime_client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME, ContentType='text/csv', Body=payload_csv
    )
    result = response["Body"].read()
    result = result.decode("utf-8")
    result = result.strip("\n0").split("\n")
    preds = list(map(float,result))
    return preds
