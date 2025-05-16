import boto3
import json

bedrock = boto3.client(service_name="bedrock")

# list all models
bedrock.list_foundation_models()

response = bedrock.list_foundation_models(byProvider="anthropic")
# response = bedrock.list_foundation_models(byProvider="Amazon")
for summary in response["modelSummaries"]:
    print(summary["modelId"])
