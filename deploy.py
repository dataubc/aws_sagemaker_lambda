import mlflow.sagemaker as mfs
from mlflow.deployments import get_deploy_client


experiment_id = 'xx'
run_id = 'xx'
region = 'xx'
aws_id = 'xxx'
arn = 'arn:aws:iam:xxx:role/aws-sagemaker-deploy'
app_name = 'model-application'
model_uri = './model/classifier'
tag_id = '2.0.1'
instance_type = "ml.m4.xlarge"

image_url = 'xx.dkr.ecr.ca-central-1.amazonaws.com/mlflow-pyfunc'



config=dict(
    assume_role_arn=arn,
    image_url=image_url,
    region_name=region,
    archive=False,
    instance_type=instance_type,
    instance_count=1,
    bucket_name='sagemaker-region-accountId'
)
client = get_deploy_client("sagemaker")
# client.create_deployment(
#     "mlflow-deployment",
#     model_uri=model_uri,
#     flavor="python_function",
#     config=config
# )

client.create_deployment(
    "mlflow-deployment2",
    model_uri=model_uri,
    flavor="python_function",
    config=config,
    endpoint = 'mlflow-deployment2'
)

# mfs.deploy(app_name,
# 	model_uri=model_uri,
# 	region_name=region,
# 	mode='create',
# 	execution_role_arn=arn,
# 	image_url=image_url)
