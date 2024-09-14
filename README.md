# Guidance for Enhanced Product Catalog with Generative AI on AWS

## Table of Contents

1. [Overview](#overview-required)
    - [Cost](#cost)
2. [Prerequisites](#prerequisites-required)
    - [Operating System](#operating-system-required)
3. [Deployment Steps](#deployment-steps-required)
4. [Deployment Validation](#deployment-validation-required)
5. [Running the Guidance](#running-the-guidance-required)
6. [Next Steps](#next-steps-required)
7. [Cleanup](#cleanup-required)
8. [FAQ, known issues, additional considerations, and limitations](#faq-known-issues-additional-considerations-and-limitations-optional)

## Overview

This guidance demonstrates how to leverage AWS services and Generative AI to enhance product catalogs for e-commerce applications. The architecture uses AWS services to ingest raw product data, process it using AI models, and create an enhanced product catalog with improved descriptions, titles, and extracted features.

![Architecture Diagram](assets/architecture_diagram.png)

Key components of the architecture:

1. Data Ingestion: Raw product data is sent via Amazon API Gateway or stored in an S3 bucket in JSON format.
2. Event Processing: New products in S3 trigger an event notification to populate an Amazon SQS queue.
3. Data Lookup: AWS Lambda functions consume messages from SQS or API Gateway, performing lookups in DynamoDB for processing rules.
4. Workflow Orchestration: AWS Step Functions manage the enhancement process.
5. AI Processing: AWS Lambda functions use Amazon Bedrock (Claude 3) to enhance product titles, descriptions, and extract features.
6. Data Storage: Enhanced product data is stored in Amazon OpenSearch Service Serverless for efficient querying and retrieval.

### Cost

You are responsible for the cost of the AWS services used while running this Guidance. As of March 2024, the cost for running this Guidance with the default settings in the US East (N. Virginia) Region is approximately $500.00 per month for processing 1,000,000 products.

We recommend creating a [Budget](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) through [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) to help manage costs. Prices are subject to change. For full details, refer to the pricing webpage for each AWS service used in this Guidance.

### Sample Cost Table

The following table provides a sample cost breakdown for deploying this Guidance with the default parameters in the US East (N. Virginia) Region for one month.

| AWS service | Dimensions | Cost [USD] |
|-------------|------------|------------|
| Amazon API Gateway | 1,000,000 REST API calls per month | $3.50 |
| Amazon S3 | 100 GB storage, 1,000,000 PUT requests | $2.30 |
| Amazon SQS | 1,000,000 requests | $0.40 |
| AWS Lambda | 1,000,000 invocations, 1GB memory, 1 second duration | $16.67 |
| Amazon DynamoDB | 1 GB storage, 1,000,000 read/write requests | $1.25 |
| AWS Step Functions | 1,000,000 state transitions | $25.00 |
| Amazon Bedrock (Claude 3) | 1,000,000 inference requests | $400.00 |
| Amazon OpenSearch Service Serverless | 100 GB storage, 1,000,000 indexing requests | $50.00 |
| Total | | $499.12 |

## Prerequisites

### Operating System

These deployment instructions are optimized to best work on Amazon Linux 2 AMI. Deployment in another OS may require additional steps.

Required packages:
- AWS CLI (version 2.0 or later)
- Node.js (version 14.x or later)
- npm (version 6.x or later)
- Python (version 3.8 or later)
- pip (version 20.x or later)

To install these packages on Amazon Linux 2, run the following commands:

```bash
sudo yum update -y
sudo yum install -y aws-cli
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
sudo yum install -y nodejs
sudo yum install -y python3 python3-pip
```

### AWS account requirements

- Ensure you have the necessary permissions to create and manage the required AWS services.
- Enable Amazon Bedrock in your AWS account and request access to the Claude 3 model.

### aws cdk bootstrap

This Guidance uses AWS CDK. If you are using AWS CDK for the first time, perform the following bootstrapping:

```bash
npm install -g aws-cdk
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

## Deployment Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/product-catalog-enhancement.git
   cd product-catalog-enhancement
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install CDK dependencies:
   ```bash
   npm install
   ```

5. Review and update the `cdk.json` file with your desired configuration parameters.

6. Deploy the CDK stack:
   ```bash
   cdk deploy
   ```

7. Note the outputs from the CDK deployment, including the API Gateway URL and other resource ARNs.

## Deployment Validation

1. Open the AWS CloudFormation console and verify that the stack with the name "ProductCatalogEnhancementStack" has been created successfully with a status of "CREATE_COMPLETE".

2. Run the following AWS CLI command to describe the stack and verify its status:
   ```bash
   aws cloudformation describe-stacks --stack-name ProductCatalogEnhancementStack
   ```

3. Check the Amazon API Gateway console to ensure the API has been created and is deployed.

4. Verify that the S3 bucket, SQS queue, DynamoDB table, and OpenSearch domain have been created in their respective consoles.

## Running the Guidance

1. To test the product enhancement process via API Gateway:
   
   a. Use the following curl command, replacing `{api-gateway-url}` with the actual URL from the deployment outputs:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"productId": "123", "title": "Basic T-Shirt", "description": "A simple cotton t-shirt", "features": ["cotton", "short sleeve"]}' https://{api-gateway-url}/prod/enhance
   ```

   b. You should receive a response with a job ID. Use this ID to check the status of the enhancement process.

2. To test the bulk processing via S3:
   
   a. Upload a JSON file containing product data to the created S3 bucket.
   b. Check the SQS queue to verify that a message has been added.
   c. Monitor the AWS Step Functions console to see the workflow execution.

3. After processing, query the OpenSearch domain to retrieve the enhanced product data:
   ```bash
   curl -X GET "https://{opensearch-domain-endpoint}/products/_search?q=productId:123"
   ```

Expected output will include the enhanced product title, description, and extracted features.

## Next Steps

- Customize the AI prompts in the Lambda functions to better suit your specific product catalog needs.
- Implement additional data validation and error handling in the ingestion process.
- Set up monitoring and alerting for the various components of the architecture.
- Explore integrating the enhanced product catalog with your e-commerce frontend or recommendation systems.

## Cleanup

To avoid incurring future charges, delete the resources created by this Guidance:

1. Empty the S3 bucket created by the stack.

2. Delete the CDK stack:
   ```bash
   cdk destroy
   ```

3. Confirm the deletion when prompted.

4. Verify in the AWS CloudFormation console that the stack has been successfully deleted.

## FAQ, known issues, additional considerations, and limitations

**Known issues:**
- The Bedrock API may have rate limits that could affect processing speed for large catalogs. Consider implementing retry logic and backoff strategies in the Lambda functions.

**Additional considerations:**
- This Guidance creates public API Gateway endpoints. Ensure proper authentication and authorization mechanisms are in place for production use.
- The OpenSearch domain is created with default settings. Adjust the instance type and storage based on your expected data volume and query patterns.

For any feedback, questions, or suggestions, please use the issues tab under this repository.
