
# Shoe Store Serverless API

This project is a serverless backend for a shoe store, built with AWS CDK, Lambda, API Gateway, DynamoDB, and S3.

## Architecture



The API is built using the following AWS services:
- **AWS API Gateway:** Manages RESTful API endpoints.
- **AWS Lambda:** Hosts the business logic (written in Python 3.12).
- **AWS DynamoDB:** Provides NoSQL data storage for shoes and orders.
- **Amazon S3:** Stores generated JSON invoices.
- **AWS CDK:** Defines the infrastructure as code.

## Prerequisites

- AWS Account & configured AWS CLI
- Node.js (for AWS CDK)
- Python 3.12+
- AWS CDK Toolkit (`npm install -g aws-cdk`)

## Deployment Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/anacrb/above-challenge.git
    cd above-challenge
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Bootstrap your AWS environment (only needed once per region):**
    ```bash
    cdk bootstrap
    ```

4.  **Deploy the stack:**
    ```bash
    cdk deploy
    ```
    The CDK will output the API Gateway endpoint URL upon successful deployment.

## API Endpoints

### List Shoes

- **GET** `/shoes`
- **GET** `/shoes?brand=<brand_name>`

**Example:**
```bash
curl "https://b3lf2ywqv7.execute-api.us-east-1.amazonaws.com/prod/shoes?brand=Nike"
```

### Create Order

- **POST** `/orders`

**Example Request Body:**
```json
{
    "username": "jane.doe",
    "shoeId": "shoe-001",
    "size": 42,
    "shipping": {
        "address": "456 Oak Ave",
        "zip": "45678"
    }
}
```

**Example Curl:**
```bash
curl -X POST \
  https://b3lf2ywqv7.execute-api.us-east-1.amazonaws.com/prod/orders \
  -H 'Content-Type: application/json' \
  -d '{                                                                                                                 
    "username": "jane.doe",
    "items": [
        { "shoeId": "shoe-001", "size": 42 },
        { "shoeId": "shoe-004", "size": 39 }
    ],
    "shipping": {
        "address": "123 Main St, Anytown",
        "zip": "12345"
    }
}'

```

### List Orders by Username

- **GET** `/orders/{username}`

**Example:**
```bash
curl https://b3lf2ywqv7.execute-api.us-east-1.amazonaws.com/prod/orders/jane.doe
```