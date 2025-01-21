# Retail Product Enhancer: Feature Extraction
# This Lambda function takes a product description as input and returns a JSON with product's features.
# It uses Amazon Bedrock to generate the features JSON based on the input description and a prompt.
import json
import boto3
from botocore.exceptions import ClientError

# Set the model ID, e.g., Claude 3 Sonnet.
model_id = "us.anthropic.claude-3-sonnet-20240229-v1:0"


def lambda_handler(event, context):
    # Get the input description from the event
    rawdata = event['raw-data']

    # Create a Bedrock Runtime client
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Define the prompt for the language model
    prompt = '''Analyze the following product description and extract key features. Output a JSON object with the following structure:
{
  "features": [
    {
      "category": "string",
      "value": "string"
    }
  ]
}

Categories may include, but are not limited to: material, color, size, weight, dimensions, capacity, compatibility, functionality, or any other relevant characteristic.

Ensure each feature is concise and specific. Limit to the most important features. Respond with only the JSON object, no additional text.

Product description:\n
''' + rawdata

    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.8,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read().decode('utf-8'))

    # Extract and print the response text.
    generated_features = model_response["content"][0]["text"]

    # Extract the generated title from the response
    # generated_title = response['Body'].read().decode('utf-8')

    # Return the generated title
    return json.loads(generated_features)