import json
from models import OrderModel

def handler(event, context):
    try:
        path_params = event.get('pathParameters')

        if not path_params or 'username' not in path_params:
            return {'statusCode': 400, 'body': json.dumps(f"Missing username parameter")}

        username = path_params['username']
        result = OrderModel.username_index.query(username)

        orders = [item.attribute_values for item in result]

        return {
            'statusCode': 200,
            'body': json.dumps(orders, indent=2, default=str)
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}
