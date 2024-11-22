# Retail Product Enhancer: Push info to Openserch Serverless domain
# This Lambda Function gets output from Title, Description and Features and push to Opensearch Serverless
# It receive's output from StepFunctions

import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from botocore.exceptions import ClientError


def lambda_handler(event, context):

    #opensearch serverless paramenters
    service = "aoss"
    region = "us-east-1"
    host =  os.environ['ENDPOINT']
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, service)
    

    #data passed from Opensearch
    title = event['title']
    description = event['description']
    features = event['features']
    
    print(host)

    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
    )
    index = 'products'
    body = {
        'title': title,
        'description': description,
        'features': features
    }
    try:
        if not client.indices.exists(index="products"):
            index_body = {
              'settings': {
                'index': {
                  'number_of_shards': 4
                }
               }
            }
            response = client.indices.create(index, body=index_body)

        response = client.index(index=index, body=body)
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except ClientError as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
