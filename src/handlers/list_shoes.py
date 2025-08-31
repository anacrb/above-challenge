import os
import json
from models import ShoeModel
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['SHOES_TABLE_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        query_params = event.get('queryStringParameters')

        if query_params and 'brand' in query_params:
            # Query by brand if provided
            brand = query_params['brand']
            response = ShoeModel.brand_index.query(brand)
        else:
            # Otherwise, return all shoes
            response = ShoeModel.scan()

        shoes = [item.attribute_values for item in response]

        for shoe in shoes:
            if 'sizes' in shoe and isinstance(shoe['sizes'], set):
                shoe['sizes'] = list(shoe['sizes'])


        print(shoes)

        return {
            'statusCode': 200,
            'body': json.dumps(shoes)
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}