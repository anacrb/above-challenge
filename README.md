
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
- Poetry for Python dependency management. 
- Docker: The build script relies on Docker, which must be running on your machine.

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
    # Install the CDK's Python dependencies
    pip install -r requirements.txt
    ```
3. **Build the lambda functions:**
    ```bash
    # Make the build script executable (only needed once)
    chmod +x ./build.sh

    # Run the build script
    ./build.sh
   ```

4. **Bootstrap your AWS environment (only needed once per region):**
    ```bash
    cdk bootstrap
    ```

5. **Deploy the stack:**
    - Deploy all stacks(Initial deploy)
    ```bash
    cdk deploy --all
    ```
   - Deploy only one stack(eg. CreateOrderStack)
    ```bash
    cdk deploy CreateOrderStack
    ```
   
   The CDK will output the API Gateway endpoint URL upon successful deployment.


6. Tear Down the stack
    - Destroy the entire stack
    ```bash
    cdk destroy --all
    ```
   - Destroy only one stack(eg. CreateOrderStack)
   ```bash
   cdk destroy CreateOrderStack
   ```

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