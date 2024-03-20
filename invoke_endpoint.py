import boto3
import io

def invoke_endpoint_csv(endpoint_name, input_data_csv):
    """
    Invoke SageMaker endpoint with CSV input.
    """
    runtime_client = boto3.client("runtime.sagemaker")
    response = runtime_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='text/csv',  # Set content type to CSV
        Body=input_data_csv  # Pass CSV data
    )
    result = response['Body'].read().decode('utf-8')
    return result

endpoint_name = "name"

# Example CSV input data: Convert your input data into a CSV string format
# Note: Ensure there are no headers and the values are comma-separated
input_data_csv = "0.5,1.2,3.4,-1.2,0.5,-0.6,1.4,-0.2,2.1,0.1,0.3,-1.1,2.0,1.2,-0.1,0.5,-0.7,1.3,-2.1,0.4,1.1,-0.3,1.5,-1.0,0.9,-0.2,1.2,0.3"

result = invoke_endpoint_csv(endpoint_name, input_data_csv)
print(result)
