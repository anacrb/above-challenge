import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['SHOES_TABLE_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        query_params = event.get('queryStringParameters')

        if query_params and 'brand' in query_params:
            # Query by brand if provided
            brand = query_params['brand']
            response = table.query(IndexName='brand-index', KeyConditionExpression=Key('brand').eq(brand))
        else:
            # Otherwise, return all shoes
            response = table.scan()

        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Items', []))
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}