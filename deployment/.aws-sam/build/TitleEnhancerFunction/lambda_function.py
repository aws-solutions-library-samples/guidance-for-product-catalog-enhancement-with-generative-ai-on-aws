# Retail Product Enhancer: Title
# This Lambda function takes a product title as input and returns a modified version of the title generated using a language model.
# It uses Amazon Bedrock to generate the modified title based on the input title and a prompt.
import json
import boto3
from botocore.exceptions import ClientError

# Set the model ID, e.g., Claude 3 Haiku.
model_id = "us.anthropic.claude-3-sonnet-20240229-v1:0"


def lambda_handler(event, context):
    print(event)
    print(context)

    # Get the input title from the event
    title = event['raw-data']

    # Create a Bedrock Runtime client
    client = boto3.client("bedrock-runtime", region_name="us-east-1")


    # Define the prompt for the language model
    prompt = f"Improve this product title to boost sales. Make it compelling, descriptive, and searchable. Include key features and benefits. Limit to 60 characters max. Respond with only the improved title.\n\nOriginal title: '{title}'"

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
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    generated_title = model_response["content"][0]["text"]
    print(generated_title)

    # Extract the generated title from the response
    # generated_title = response['Body'].read().decode('utf-8')

    # Return the generated title
    return {
        'title': generated_title
    }